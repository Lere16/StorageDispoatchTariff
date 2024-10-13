# GAMSPY version-----------------------------------------------------------------

from gamspy import (
    Container,
    Set,
    Parameter,
    Variable,
    Equation,
    Model,
    Sum,
    Ord,
)
from gamspy.math import exp, abs
import pandas as pd
import numpy as np
import os
import sys

from utils.datastructs import OptResult

# HELPER FUNCTIONS:-------------------------------------------------------

# for nodal pricing 
''' 
def filter_data(price_table, node):

    nodal_price = price_table.loc[
        price_table.node == node, ["t", "k", "marginal"]
    ]
    df_sorted = nodal_price.sort_values(by=["k", "t", "marginal"])
    df_sorted = df_sorted.drop(["k", "t"], axis=1)
    df_sorted.reset_index(inplace=True, drop=True)
    df_sorted["hour"] = df_sorted.index
    return df_sorted
'''
def filter_data(price_table):

    nodal_price = price_table[["t", "k", "marginal"]]
    df_sorted = nodal_price.sort_values(by=["k", "t", "marginal"])
    df_sorted = df_sorted.drop(["k", "t"], axis=1)
    #df_sorted.to_csv(os.path.join('results/CSV', "cost_2014.csv"), index=False)
    df_sorted.reset_index(inplace=True, drop=True)
    df_sorted["hour"] = df_sorted.index
    return df_sorted


def filter_gridload(df_load, node):

    df_load = df_load.loc[df_load.node == node, ["t", "k", "value"]]
    df_sorted = df_load.sort_values(by=["k", "t", "value"])
    df_sorted.to_csv(os.path.join('results/CSV', "load_2014.csv"), index=False)
    df_sorted = df_sorted.drop(["k", "t"], axis=1)
    df_sorted.reset_index(inplace=True, drop=True)
    return df_sorted

def calculate_slope(g, Cthres):
    y = g.values
    a = np.sum(y)
    b_sum = 0
    for val in y:
        if val > Cthres:
            b_sum += (val - Cthres) * val
    slop = a / b_sum
    
    return slop

#End helper functions 

def bat_optimize_(params, price_table, df_load, scenario, size, base_tariff, VOLL, delta, node):
    
    #node=params['scenario_1']['global']['network']['node']
    tariff_status=params[scenario]['global']['tariff']['tariff_status']
    
    storage_duration = float(params['scenario_1']['global']['parameter']['storage_duration'])  # 4 hours of storage duration
    
    Rmax= size / storage_duration
    charge_eff = float(params['scenario_1']['global']['parameter']['charge_eff'])
    discharge_eff = float(params['scenario_1']['global']['parameter']['discharge_eff'])
    annual_OM = float(params['scenario_1']['global']['storage']['annual_OM'])*Rmax 
    lifetime = float(params['scenario_1']['global']['storage']['lifetime'])
    annual_cap_cost = float(params['scenario_1']['global']['storage']['cap_cost'])*size /lifetime
    DoD = float(params['scenario_1']['global']['parameter']['DoD'][:-1])/1e2
    reserve = float(params['scenario_1']['global']['parameter']['reserve'][:-1])/1e2
    configuration = params[scenario]['global']['tariff']['configuration'] 
    
    #Filter the data
    df= filter_data(price_table) # TODO add "node" and call the appropriate function in case of nodal pricing 
    nodal_load = filter_gridload(df_load, node).value
    
    
    # Convert marginal price to EUR/ kWh
    #df['marginal'] /= 1e3
    #Convert load to kWh
    #nodal_load *=1e3
    
    #MODEL INITIALIZATION
    #bat = Container(working_directory=os.path.join(os.getcwd(), "debugg_bat"))
    bat = Container(
        system_directory=os.getenv("SYSTEM_DIRECTORY", None),
        delayed_execution=int(os.getenv("DELAYED_EXECUTION", False)),
    )

    # WITHOUT Tariff functions 
    t=Set(bat, name = "t", records = df.hour.tolist(), description = " hours")
    P=Parameter(bat,"P", domain=[t], records=df['marginal'], description="marginal price")
    
    # Variables
    SOC = Variable(bat, name="SOC", type="free", domain=t)
    Pd = Variable(bat, name="Pd", type="Positive", domain=t)
    Pc = Variable(bat, name="Pc", type="Positive", domain=t)
    
    obj = Variable(
        bat, name="obj", type="free", description="Objective function"
    )
    
    #SCALARS
    SOC0 = Parameter(bat, name="SOC0", records=size/2)
    SOCmax = Parameter(bat, name="SOCmax", records=size)
    SOCmin = Parameter(bat, name="SOCmin", records=reserve*size)
    eta_c = Parameter(bat, name="eta_c", records= charge_eff)
    eta_d = Parameter(bat, name="eta_d", records= discharge_eff)
    
    SOC.up[t] = SOCmax
    SOC.lo[t] = SOCmin
    
    Pc.up[t] = SOCmax/storage_duration
    Pc.lo[t] = 0
    Pd.up[t] = SOCmax/storage_duration
    Pd.lo[t] = 0
    
    # EQUATION 
    constESS = Equation(bat, name="constESS", type="regular", domain=t)
    defobj = Equation(bat, "defobj")
    
    
    constESS[t] = (
        SOC[t]
        == SOC0.where[Ord(t) == 1]
        + SOC[t.lag(1)].where[Ord(t) > 1]
        + Pc[t] * eta_c
        - Pd[t] / eta_d
    )
    
    # Avoid charging and dishcraging at the same time
    
    chargestate = Variable(bat, 'chargestate', domain=[t], type='binary')
    defcharge = Equation(bat, name="defcharge", type="regular", domain=t)
    defdischarge = Equation(bat, name="defdischarge", type="regular", domain=t)
    
    defcharge[t] = Pc[t] <= chargestate[t] * Pc.up[t]
    defdischarge[t] = Pd[t] <= (1-chargestate[t]) * Pd.up[t]
    
    
    # Calculate net load 
    net_load = Variable(bat, 'net_load', domain=[t], type='free')
    defnetload = Equation(bat, name="netload", domain=[t])
    gridload = Parameter(bat, 'gridload', domain=[t], records= nodal_load)
    
    if configuration == "ex-post":
        defnetload[t] = net_load[t] == gridload[t] + Pc[t] - Pd[t]
    elif configuration == "ex-ante":
        defnetload[t] = net_load[t] == gridload[t]
        
    scale_val=1e4
    #net_load.scale[t]=scale_val
    
    # WITH tariff functions
    tariff_level = Variable(bat, 'tarrif_level', domain=[t], type='Positive')
    
    #Initilaize cap_limit and cap_threshold for info dictionnary 
    cap_limit = 1.2*nodal_load.max(axis=0)
    cap_threshold = (1-delta)*nodal_load.max(axis=0)
    
    #limit net load to the network limit capacity
    # Calculate net load 
    total_load = Variable(bat, 'total_load', domain=[t], type='free')
    deftotalload = Equation(bat, name="deftotalload", domain=[t])
    deftotalload[t] = total_load[t] == gridload[t] + Pc[t]
    total_load.up[t]=cap_limit
    
    #avoid negative net load
    load_injection = Variable(bat, 'load_injection', domain=[t], type='free')
    defload_injection = Equation(bat, name="defload_injection", domain=[t])
    defload_injection[t] = load_injection[t] == gridload[t] - Pd[t]
    load_injection.lo[t]=0
    
    
    if tariff_status == 'on':
        
        # Read scalars from params
        shape=params[scenario]['global']['tariff']['shape']
        share=float(params[scenario]['global']['tariff']['share']) # added
        #EUR_base = base_tariff/1e3
        EUR_base = base_tariff
        EUR_high = VOLL
    
        
        if shape == "flat":
            
            tariff_level.fx[t]= EUR_base
        
            ''' 
            defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level[t]))-(annual_cap_cost + annual_OM)
        
            opt = Model(
                    bat,
                    name="opt",
                    equations=bat.getEquations(),
                    problem="MIQCP",
                    sense="MAX",
                    objective=obj,
                )
            opt.solve(solver="CPLEX", solver_options={'optimalitytarget': 3, 'subalg': 4, 'mipdisplay': 5, 'mipgap':0.03})
                        
            '''
        elif shape == "piecewise":
             
            # cap_limit and cap_threshold based on grid load
            cap_limit = 1.2*nodal_load.max(axis=0)
            cap_threshold = (1-delta)*nodal_load.max(axis=0)
        
            x1 = -cap_limit
            x2 = -cap_threshold
            x3 = cap_threshold
            x4 = cap_limit
            
            
            y1 = -EUR_high
            y2 = EUR_base
            y3 = EUR_base
            
        
            #3 segments 
            # New set and parameter, and variables for peicewise 
            s = Set(bat, 's', records=['s1','s2','s3'])
            sx = Parameter(bat, 'sx', domain=[s], records=[ ['s1',x1], ['s2',x2], ['s3',x3]])
            sy = Parameter(bat, 'sy', domain=[s], records=[ ['s1',y1], ['s2',y2*(1-share)], ['s3',y3*(1-share)]])
            sslope = Parameter(bat, 'sslope', domain=[s])
            
            sslope['s1'] = calculate_slope(nodal_load, x3)*EUR_base*share
            sslope['s2'] = (y3-y2)*(1-share)/(x3-x2)
            sslope['s3'] = calculate_slope(nodal_load, x3)*EUR_base*share
            
            sselect = Variable(bat, 'sselect', domain=[t,s], type='binary')
            sstep = Variable(bat, 'sstep', domain=[t,s], type='Positive')
            sstep.up[t,'s1'] = x2-x1
            sstep.up[t,'s2'] = x3-x2
            sstep.up[t,'s3'] = x4-x3
        
            # Equations
            oneSeg = Equation(bat, name="oneSeg", domain=[t])
            defy = Equation(bat, name="defy", domain=[t])
            defx = Equation(bat, name="defx", domain=[t])
            defslope = Equation(bat, name="defslope", domain=[t,s])
            
            oneSeg[t] = Sum(s, sselect[t,s]) == 1
            defy[t] = tariff_level[t] == Sum(s, sy[s]*sselect[t,s] + sstep[t,s]*sslope[s])
            defx[t] = net_load[t] == Sum(s, sx[s]*sselect[t,s] + sstep[t,s])
            defslope[t,s] = sstep[t,s] <= sstep.up[t,s]*sselect[t,s] 
            
            
            ''' 
            #2 segments 
            # New set and parameter, and variables for peicewise 
            s = Set(bat, 's', records=['s2','s3'])
            sx = Parameter(bat, 'sx', domain=[s], records=[ ['s2',x2], ['s3',x3]])
            sy = Parameter(bat, 'sy', domain=[s], records=[['s2',y2*(1-share)], ['s3',y3*(1-share)]])
            sslope = Parameter(bat, 'sslope', domain=[s])
            
            sslope['s2'] = (y3-y2)*(1-share)/(x3-x2)
            sslope['s3'] = calculate_slope(nodal_load, x3)*EUR_base*share
            
            sselect = Variable(bat, 'sselect', domain=[t,s], type='binary')
            sstep = Variable(bat, 'sstep', domain=[t,s], type='Positive')
            sstep.up[t,'s2'] = x3-x2
            sstep.up[t,'s3'] = (x4-x3)
        
            # Equations
            oneSeg = Equation(bat, name="oneSeg", domain=[t])
            defy = Equation(bat, name="defy", domain=[t])
            defx = Equation(bat, name="defx", domain=[t])
            defslope = Equation(bat, name="defslope", domain=[t,s])
            
            oneSeg[t] = Sum(s, sselect[t,s]) == 1
            defy[t] = tariff_level[t] == Sum(s, sy[s]*sselect[t,s] + sstep[t,s]*sslope[s])
            defx[t] = net_load[t] == Sum(s, sx[s]*sselect[t,s] + sstep[t,s])
            defslope[t,s] = sstep[t,s] <= sstep.up[t,s]*sselect[t,s]
            '''
            
            ''' 
            defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level.l[t])) - (annual_cap_cost + annual_OM) 
        
            opt = Model(
                bat,
                name="opt",
                equations=bat.getEquations(),
                problem="MIQCP",
                sense="MAX",
                objective=obj,
            )
            '''
            
            ''' 
            defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level[t]))-(annual_cap_cost + annual_OM)
        
            
            opt = Model(
                    bat,
                    name="opt",
                    equations=bat.getEquations(),
                    problem="MIQCP",
                    sense="MAX",
                    objective=obj,
                )
            opt.solve(solver="CPLEX", solver_options={'optimalitytarget': 3, 'subalg': 4, 'mipdisplay': 5, 'mipgap':0.03, 'timelimit': 1800, 'mipemphasis': 3, 'threads': 32},)
            '''
                    
        elif shape== "proportional":
            deftariff = Equation(bat, name="deftariff", domain=[t])
            #calculate slope 
            y = nodal_load.values
            slope= EUR_base*share*(np.sum(y))/np.sum(np.power(y, 2))
            
            deftariff[t] = tariff_level[t] == slope*net_load[t]+EUR_base*(1-share)
            
            ''' 
            defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level[t]))-(annual_cap_cost + annual_OM)
        
            opt = Model(
                    bat,
                    name="opt",
                    equations=bat.getEquations(),
                    problem="MIQCP",
                    sense="MAX",
                    objective=obj,
                )
            opt.solve(solver="CPLEX", solver_options={'optimalitytarget': 3, 'subalg': 4, 'mipdisplay': 5, 'mipgap':0.03, 'mipemphasis': 3, 'threads': 32}, ) # output=sys.stdout
            '''
            
        elif shape== "bigm":
            
            cap_limit = nodal_load.max(axis=0)
            cap_threshold = (1-delta)*cap_limit 
        
            x1 = -cap_limit
            x2 = -cap_threshold
            x3 = cap_threshold
            x4 = cap_limit
            
            #Binary variable
            b2 = Variable(bat, 'b2', domain=[t], type='binary')
            b3 = Variable(bat, 'b3', domain=[t], type='binary')
            
            # Big M constant
            M=1e5
            epsilon=1e-6
            
            # Constraints to ensure only one segment is active at a time
            single_seg = Equation(bat, name="single_seg", domain=[t])
            single_seg[t] = b2[t] + b3[t] == 1
            
            #Segment constraints
            deftariff2 = Equation(bat, name="deftariff2", domain=[t])
            deftariff3 = Equation(bat, name="deftariff3", domain=[t])
            
            deftariff2[t] = tariff_level[t] <= EUR_base*(1-share) + M*(1-b2[t])
            deftariff3[t] = tariff_level[t] <= calculate_slope(nodal_load, x3)*EUR_base*share*(net_load[t] - x3) + EUR_base + M*(1-b3[t]) 
            
            # Activation constraints
            
            activation1 = Equation(bat, name="activation1", domain=[t])
            activation2 = Equation(bat, name="activation2", domain=[t])
            activation3 = Equation(bat, name="activation3", domain=[t])
            activation4 = Equation(bat, name="activation4", domain=[t])
            
            activation1[t] = net_load[t] >= x2 + epsilon - M*(1-b2[t])
            activation2[t] = net_load[t] <= x3 + M*(1-b2[t])
            activation3[t] = net_load[t] >= x3 + epsilon - M*(1-b3[t])
            activation4[t] = net_load[t] <= x4 + M*(1-b3[t])
            
            ''' 
            defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level[t]))-(annual_cap_cost + annual_OM)
        
            opt = Model(
                    bat,
                    name="opt",
                    equations=bat.getEquations(),
                    problem="MIQCP",
                    sense="MAX",
                    objective=obj,
                )
            
            opt.solve(solver="CPLEX", solver_options={'optimalitytarget': 3, 'subalg': 4, 'mipdisplay': 3, 'mipgap':0.05, 'mipemphasis': 1})
            '''
            

        
        # define ojective function when tariff is on
        defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * (P[t] + tariff_level[t])) - (annual_cap_cost + annual_OM)
        
        opt = Model(
            bat,
            name="opt",
            equations=bat.getEquations(),
            problem="MIQCP",
            sense="MAX",
            objective=obj,
        )
        

    else: # objective function Without tariff
        tariff_level.fx[t]= 0.01e-15
        defobj[...] = obj == Sum(t, (Pd[t] - Pc[t]) * P[t]) - (
            annual_cap_cost + annual_OM
        )
        opt = Model(
            bat,
            name="opt",
            equations=bat.getEquations(),
            problem="MIP",
            sense="MAX",
            objective=obj,
        )
    
     
    opt.solve(solver="CPLEX", solver_options={'optimalitytarget': 3, 'subalg': 4, 'mipdisplay': 5, 'mipgap':0.03,'timelimit': 1800, 'mipemphasis': 3, 'threads': 32}, ) # output=sys.stdout
    #reporting data and parameters 
    rep = Parameter(bat, name="rep", domain=[t, "*"])
    rep[t, "Pc"] = Pc.l[t]
    rep[t, "Pd"] = Pd.l[t]
    rep[t, "SOC"] = SOC.l[t]
    rep[t, "net_load"] = net_load.l[t]
    rep[t, "tariff"] = tariff_level.l[t]
    
    data=rep.pivot()
    data['hour'] = data.index
    data['base_price'] = P.records['value'].values
    data['hour'] = data['hour'].astype(int)
    data['gridload']= gridload.records["value"].values
    status=opt.status
    objective=opt.objective_value
    info={}
    info["data"]=data
    info["capacity limit"]=cap_limit
    info["capacity threshold"]=cap_threshold

    
    return OptResult(status, objective, None, None, info, None)
    
    
    


    