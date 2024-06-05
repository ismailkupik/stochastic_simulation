import pandas as pd
import math



def optimal_t_and_S_level_for_deterministic_model(setup_time_for_A,setup_time_for_B,lambda_for_A,lambda_for_B,Mu_for_A,Mu_for_B,setup_cost_for_A,setup_cost_for_B,holding_cost_for_A,holding_cost_for_B,backorder_cost_for_A,backorder_cost_for_B):
    p_A = lambda_for_A/Mu_for_A
    p_B = lambda_for_B/Mu_for_B 
    T_min= (setup_time_for_A+setup_time_for_B)/(1-(p_A+p_B))


    K = setup_cost_for_A+ setup_cost_for_B



    equation_1 = 2*(K - ((setup_time_for_A+setup_time_for_B)**2/(2*((1-p_A)/(lambda_for_A*holding_cost_for_A)+(1-p_B)/(lambda_for_B*holding_cost_for_B)))))
    
    equation_2 =(((1-p_A)*lambda_for_A*holding_cost_for_A*backorder_cost_for_A/(holding_cost_for_A+backorder_cost_for_A))-((1-p_A-p_B)**2/((1-p_A)/(lambda_for_A*holding_cost_for_A)+(1-p_B)/(lambda_for_B*holding_cost_for_B)))) 

    equation_3 = (((1-p_B)*lambda_for_B*holding_cost_for_B*backorder_cost_for_B/(holding_cost_for_B+backorder_cost_for_B))-((1-p_A-p_B)**2/((1-p_A)/(lambda_for_A*holding_cost_for_A)+(1-p_B)/(lambda_for_B*holding_cost_for_B)))) 

    T_d = (equation_1/(equation_2+equation_3))**0.5

    T_optimal= max(T_min,T_d)

    T_A_optimal = p_A*T_optimal + ((1-p_A)/(lambda_for_A*holding_cost_for_A)) * ((1-(setup_time_for_A+setup_time_for_B)/T_optimal-p_A-p_B)/((1-p_A)/(lambda_for_A*holding_cost_for_A)+(1-p_B)/(lambda_for_B*holding_cost_for_B)))*T_optimal
    T_B_optimal = p_B*T_optimal + ((1-p_B)/(lambda_for_B*holding_cost_for_B)) * ((1-(setup_time_for_A+setup_time_for_B)/T_optimal-p_A-p_B)/((1-p_A)/(lambda_for_A*holding_cost_for_A)+(1-p_B)/(lambda_for_B*holding_cost_for_B)))*T_optimal


    S_A_optimal = -T_A_optimal*lambda_for_A+ T_optimal*lambda_for_A*(p_A*holding_cost_for_A+backorder_cost_for_A)/(holding_cost_for_A+backorder_cost_for_A)
    if S_A_optimal < 1:
        S_A_optimal = 1 
    else:
        S_A_optimal = math.ceil(S_A_optimal)
        
    S_B_optimal = -T_B_optimal*lambda_for_B+ T_optimal*lambda_for_B*(p_B*holding_cost_for_B+backorder_cost_for_B)/(holding_cost_for_B+backorder_cost_for_B)
    if S_B_optimal < 1:
        S_B_optimal = 1 
    else:
        S_B_optimal = math.ceil(S_B_optimal)


    return T_A_optimal, T_B_optimal,S_A_optimal,S_B_optimal, T_optimal





df = pd.read_excel('experiment_table_input-yeni_h_b.xlsx')



for i in range(len(df)):
    optimal_s_t_levels = optimal_t_and_S_level_for_deterministic_model(df.loc[i,"a_1"],df.loc[i,"a_2"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"K"],df.loc[i,"K"],df.loc[i,"h_1"],df.loc[i,"h_2"],df.loc[i,"b_1"],df.loc[i,"b_2"])
    df.loc[i,"T*"] = optimal_s_t_levels[4]
    df.loc[i,"T_1*"] = optimal_s_t_levels[0]
    df.loc[i,"T_2*"] = optimal_s_t_levels[1]
    df.loc[i,"S_1*"] = optimal_s_t_levels[2]
    df.loc[i,"S_2*"] = optimal_s_t_levels[3]


df.to_excel('experiment_table_2.xlsx', index=False)  
