import pandas as pd 
import numpy as np
import random
import statistics
def simulation_model(holding_cost_for_A,back_order_cost_for_A,setup_cost_for_A_to_B,holding_cost_for_B,back_order_cost_for_B,setup_cost_for_B_to_A,cycle,order_up_to_level_for_A,order_up_to_level_for_B,A_production_parameter, B_production_parameter,setup_time_for_A_to_B, setup_time_for_B_to_A, A_demand_parameter,B_demand_parameter ):
    holding_cost_for_A = holding_cost_for_A   #dakikalık cost    
    back_order_cost_for_A = back_order_cost_for_A  #dakikalık cost
    setup_cost_for_A_to_B = setup_cost_for_A_to_B
    holding_cost_for_B = holding_cost_for_B #dakikalık cost
    back_order_cost_for_B = back_order_cost_for_B  #dakikalık cost
    setup_cost_for_B_to_A = setup_cost_for_B_to_A
    cycle = cycle  #dakika cinsinden [400,400] şöyle bir görünümü olacak
    order_up_to_level_for_A = order_up_to_level_for_A
    order_up_to_level_for_B = order_up_to_level_for_B
    A_production_parameter = A_production_parameter*60  #saatlik Mu
    B_production_parameter = B_production_parameter*60 #saatlik Mu
    setup_time_for_A_to_B = setup_time_for_A_to_B  #dakika cinsinden
    setup_time_for_B_to_A = setup_time_for_B_to_A #dakika cinsinden
    A_demand_parameter = A_demand_parameter*60   #saatlik lambda
    B_demand_parameter = B_demand_parameter*60   #saatlik lambda



    simulation_length = 20  #maksimum simulation length






    df_columns = {
        'Time': [],
        'Current Event': [],
        'Next Event Type': [],
        'Next Event Time': [],
        'Instantenous Demand for Product A': [],
        'Instantenous Demand for Product B': [],
        'Inventory Level for product A': [],
        'Inventory Level for product B': [],
        'Total Holding Cost':[],
        'Total Backorder Cost': [],
        'Total Setup Cost':[],
        'Total Cost':[],
        'Cumulative Demand For Product A':[],
        'Cumulative Demand For Product B':[],

    }

    df = pd.DataFrame(df_columns)



    def calculate_minutes_difference(current_time_str, previous_event_time_str):
        # Mevcut zamanı ve önceki olay zamanını pandas Timestamp olarak ayarla
        current_time = pd.Timestamp(current_time_str)
        previous_event_time = pd.Timestamp(previous_event_time_str)
        # Zaman farkını hesapla
        time_difference = current_time - previous_event_time
        # Zaman farkını dakika cinsinden hesapla
        minutes_difference = time_difference.total_seconds() / 60
        return minutes_difference




    current_time = pd.Timestamp('08:00:00')
    def add_time_and_adjust(current_time_str, minutes_to_add):
        current_time = pd.Timestamp(current_time_str)
        # Zamanı dakika cinsinden doğrudan ekle
        result_time = current_time + pd.Timedelta(minutes=minutes_to_add)
        return result_time



    end_time_of_cycle_parts = []
    for i in range(simulation_length):
        if i == 0:
            end_time_of_cycle_parts.append(add_time_and_adjust(current_time,cycle[0]))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],setup_time_for_A_to_B))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],cycle[1]))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],setup_time_for_B_to_A))
            
        else:
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],cycle[0]))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],setup_time_for_A_to_B))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],cycle[1]))
            end_time_of_cycle_parts.append(add_time_and_adjust(end_time_of_cycle_parts[-1],setup_time_for_B_to_A))



    current_process = "-"
    next_event = "-"
    instantenous_demand_for_product_A = 0 
    instantenous_demand_for_product_B = 0 
    inventory_level_for_product_A = 20
    inventory_level_for_product_B = 20
    total_holding_cost_for_product_A = 0
    total_holding_cost_for_product_B = 0
    total_holding_cost = 0 
    total_back_order_cost_for_A = 0 
    total_back_order_cost_for_B = 0 
    total_back_order_cost = 0 
    total_setup_cost = 0
    starting_time = pd.Timestamp('08:00:00')
    previous_event_time = pd.Timestamp('08:00:00')
    cumulative_demand_for_product_A = 0 
    cumulative_demand_for_product_B = 0 
    highest_inventory_level_for_product_A = 0 
    highest_inventory_level_for_product_B = 0
    highest_awaiting_demand_for_product_A = 0
    highest_awaiting_demand_for_product_B = 0

    number_of_customer_request_met_immediately_for_A = 0  #talep geldiği gibi karşılanan müşteri sayısı
    number_of_customer_request_met_immediately_for_B = 0 

    number_of_customer_request_met_subsequently_for_A = 0 #talep geldiği gibi karşılanamayan müşteri sayısı
    number_of_customer_request_met_subsequently_for_B = 0 


    order_up_to_level_situation_for_A = 0 
    order_up_to_level_situation_for_B = 0


    simulation_continue = True
    cycle_average_cost_list = []
    cycle_start_time = starting_time
    total_cost_in_the_cycle_start = 0 

    for k in range(simulation_length):
        if simulation_continue == True:
            while current_time < end_time_of_cycle_parts[k*4]  :
                    if inventory_level_for_product_A >= (order_up_to_level_for_A-1):
                        next_production_time_for_A = add_time_and_adjust(current_time, 100000)
                        order_up_to_level_situation_for_A = 1 
                    if inventory_level_for_product_A < (order_up_to_level_for_A-1):
                        if next_event =="-" and k == 0:
                            next_production_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_production_parameter * 60) )
                        if next_event == "Production of A":
                            next_production_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_production_parameter * 60) )
                        if order_up_to_level_situation_for_A==1 :
                            next_production_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_production_parameter * 60) )
                            order_up_to_level_situation_for_A = 0 
                    if next_event =="-" and k == 0:
                        next_demand_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_demand_parameter * 60) )
                    if next_event =="Demand of A":
                        next_demand_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_demand_parameter * 60) )

                    if next_event =="-" and k == 0:
                        next_demand_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_demand_parameter * 60) )
                    if next_event =="Demand of B":
                        next_demand_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_demand_parameter * 60) )

                    if next_production_time_for_A < next_demand_time_for_A and next_production_time_for_A< next_demand_time_for_B:
                        if next_production_time_for_A < end_time_of_cycle_parts[k*4]:
                            next_event = "Production of A"
                            next_event_time = next_production_time_for_A
                        else: 
                            next_event = "Setup for production of B"
                            next_event_time = end_time_of_cycle_parts[k*4]
                    
                    if next_demand_time_for_A < next_production_time_for_A and next_demand_time_for_A< next_demand_time_for_B:
                        if next_demand_time_for_A < end_time_of_cycle_parts[k*4]:
                            next_event = "Demand of A"
                            next_event_time = next_demand_time_for_A
                        else: 
                            next_event = "Setup for production of B"
                            next_event_time = end_time_of_cycle_parts[k*4]

                    if next_demand_time_for_B < next_demand_time_for_A and next_demand_time_for_B< next_production_time_for_A:
                        if next_demand_time_for_B < end_time_of_cycle_parts[k*4]:
                            next_event = "Demand of B"
                            next_event_time = next_demand_time_for_B
                        else: 
                            next_event = "Setup for production of B"
                            next_event_time = end_time_of_cycle_parts[k*4]
                    total_back_order_cost_for_A =  total_back_order_cost_for_A + (back_order_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_A)
                    total_back_order_cost_for_B = total_back_order_cost_for_B +(back_order_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_B)
                    total_back_order_cost = total_back_order_cost_for_A + total_back_order_cost_for_B
                    total_holding_cost_for_product_A = total_holding_cost_for_product_A + (holding_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_A)
                    total_holding_cost_for_product_B = total_holding_cost_for_product_B + (holding_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_B)
                    total_holding_cost = total_holding_cost_for_product_A + total_holding_cost_for_product_B

                    if current_time < end_time_of_cycle_parts[k*4]: 
                        if current_process == "Production of A":
                            inventory_level_for_product_A = inventory_level_for_product_A + 1 
                        if current_process == "Demand of A":
                            instantenous_demand_for_product_A = instantenous_demand_for_product_A +1 
                            cumulative_demand_for_product_A = cumulative_demand_for_product_A+1
                            if inventory_level_for_product_A > 0:
                                number_of_customer_request_met_immediately_for_A  = number_of_customer_request_met_immediately_for_A + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_A = number_of_customer_request_met_subsequently_for_A + 1 

                        if current_process == "Demand of B":
                            instantenous_demand_for_product_B =instantenous_demand_for_product_B + 1 
                            cumulative_demand_for_product_B = cumulative_demand_for_product_B+1
                            if inventory_level_for_product_B > 0:
                                number_of_customer_request_met_immediately_for_B  = number_of_customer_request_met_immediately_for_B + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_B = number_of_customer_request_met_subsequently_for_B + 1 
                    if instantenous_demand_for_product_A >= inventory_level_for_product_A:
                        instantenous_demand_for_product_A = instantenous_demand_for_product_A-inventory_level_for_product_A
                        inventory_level_for_product_A = 0

                    else:
                        inventory_level_for_product_A = inventory_level_for_product_A - instantenous_demand_for_product_A
                        instantenous_demand_for_product_A = 0

                    if instantenous_demand_for_product_B >= inventory_level_for_product_B:
                        instantenous_demand_for_product_B = instantenous_demand_for_product_B-inventory_level_for_product_B
                        inventory_level_for_product_B = 0
                    else:
                        inventory_level_for_product_B = inventory_level_for_product_B - instantenous_demand_for_product_B
                        instantenous_demand_for_product_B = 0

                            
                    df = df.append({'Time': current_time, 'Current Event': current_process, 'Next Event Type': next_event,
                                    'Next Event Time': next_event_time,
                                    'Instantenous Demand for Product A':instantenous_demand_for_product_A,
                                    'Instantenous Demand for Product B':instantenous_demand_for_product_B,
                                    'Inventory Level for product A': inventory_level_for_product_A,
                                    'Inventory Level for product B':inventory_level_for_product_B,
                                    'Total Holding Cost':total_holding_cost,
                                    'Total Backorder Cost':total_back_order_cost,
                                    'Total Setup Cost':total_setup_cost,
                                    'Total Cost': (total_setup_cost+total_holding_cost+total_back_order_cost),
                                    'Cumulative Demand For Product A':cumulative_demand_for_product_A,
                                    'Cumulative Demand For Product B':cumulative_demand_for_product_B}, ignore_index=True) 
                    if instantenous_demand_for_product_A > highest_awaiting_demand_for_product_A:
                        highest_awaiting_demand_for_product_A = instantenous_demand_for_product_A 
                    if instantenous_demand_for_product_B > highest_awaiting_demand_for_product_B:
                        highest_awaiting_demand_for_product_B = instantenous_demand_for_product_B
                    if inventory_level_for_product_A > highest_inventory_level_for_product_A:
                        highest_inventory_level_for_product_A = inventory_level_for_product_A
                    if inventory_level_for_product_B > highest_inventory_level_for_product_B:
                        highest_inventory_level_for_product_B = inventory_level_for_product_B
                    previous_event_time = current_time
                    current_time = next_event_time
                    
                    

                    current_process = next_event





            for i in range(10):
                df = df.append({'Time': "-", 'Current Event': "-", 'Next Event Type': "-",
                                'Next Event Time':"-",
                                'Instantenous Demand for Product A':"-",
                                'Instantenous Demand for Product B':"-",
                                'Inventory Level for product A': "-",
                                'Inventory Level for product B':"-",
                                'Cumulative Demand For Product A':"-",
                                'Cumulative Demand For Product B':"-"}, ignore_index=True) 


            current_time = end_time_of_cycle_parts[k*4]      
            current_process = "-"
            next_event = "-"
            total_setup_cost = total_setup_cost + setup_cost_for_A_to_B


            while current_time < end_time_of_cycle_parts[k*4+1] :
                    if next_event  == "Demand of A":
                        next_demand_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_demand_parameter * 60) )
                    if next_event == "Demand of B":
                        next_demand_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_demand_parameter * 60) )
                    
                    
                    if  next_demand_time_for_A< next_demand_time_for_B:
                        if next_demand_time_for_A < end_time_of_cycle_parts[k*4+1]:
                            next_event = "Demand of A"
                            next_event_time = next_demand_time_for_A
                        else: 
                            next_event = "Production of B"
                            next_event_time = end_time_of_cycle_parts[k*4+1]

                    if next_demand_time_for_B < next_demand_time_for_A :
                        if next_demand_time_for_B < end_time_of_cycle_parts[k*4+1]:
                            next_event = "Demand of B"
                            next_event_time = next_demand_time_for_B
                        else: 
                            next_event = "Production of B"
                            next_event_time = end_time_of_cycle_parts[k*4+1]

                    total_back_order_cost_for_A =  total_back_order_cost_for_A + (back_order_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_A)
                    total_back_order_cost_for_B = total_back_order_cost_for_B +(back_order_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_B)
                    total_back_order_cost = total_back_order_cost_for_A + total_back_order_cost_for_B
                    total_holding_cost_for_product_A = total_holding_cost_for_product_A + (holding_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_A)
                    total_holding_cost_for_product_B = total_holding_cost_for_product_B + (holding_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_B)
                    total_holding_cost = total_holding_cost_for_product_A + total_holding_cost_for_product_B

                    if current_time < end_time_of_cycle_parts[k*4+1]: 
                        if current_process == "Demand of A":
                            instantenous_demand_for_product_A = instantenous_demand_for_product_A +1 
                            cumulative_demand_for_product_A = cumulative_demand_for_product_A+1
                            if inventory_level_for_product_A > 0:
                                number_of_customer_request_met_immediately_for_A  = number_of_customer_request_met_immediately_for_A + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_A = number_of_customer_request_met_subsequently_for_A + 1 
                        if current_process == "Demand of B":
                            instantenous_demand_for_product_B =instantenous_demand_for_product_B + 1 
                            cumulative_demand_for_product_B = cumulative_demand_for_product_B+1
                            if inventory_level_for_product_B > 0:
                                number_of_customer_request_met_immediately_for_B  = number_of_customer_request_met_immediately_for_B + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_B = number_of_customer_request_met_subsequently_for_B + 1 



                    if instantenous_demand_for_product_A >= inventory_level_for_product_A:
                        instantenous_demand_for_product_A = instantenous_demand_for_product_A-inventory_level_for_product_A
                        inventory_level_for_product_A = 0
                    else:

                        inventory_level_for_product_A = inventory_level_for_product_A - instantenous_demand_for_product_A
                        instantenous_demand_for_product_A = 0

                    if instantenous_demand_for_product_B >= inventory_level_for_product_B:
                        instantenous_demand_for_product_B = instantenous_demand_for_product_B-inventory_level_for_product_B
                        inventory_level_for_product_B = 0
                    else:
                        inventory_level_for_product_B = inventory_level_for_product_B - instantenous_demand_for_product_B
                        instantenous_demand_for_product_B = 0



                    df = df.append({'Time': current_time, 'Current Event': current_process, 'Next Event Type': next_event,
                                    'Next Event Time': next_event_time,
                                    'Instantenous Demand for Product A':instantenous_demand_for_product_A,
                                    'Instantenous Demand for Product B':instantenous_demand_for_product_B,
                                    'Inventory Level for product A': inventory_level_for_product_A,
                                    'Inventory Level for product B':inventory_level_for_product_B,
                                    'Total Holding Cost':total_holding_cost,
                                    'Total Backorder Cost':total_back_order_cost,
                                    'Total Setup Cost':total_setup_cost,
                                    'Total Cost': (total_setup_cost+total_holding_cost+total_back_order_cost),
                                    'Cumulative Demand For Product A':cumulative_demand_for_product_A,
                                    'Cumulative Demand For Product B':cumulative_demand_for_product_B}, ignore_index=True) 
                    if instantenous_demand_for_product_A > highest_awaiting_demand_for_product_A:
                        highest_awaiting_demand_for_product_A = instantenous_demand_for_product_A 
                    if instantenous_demand_for_product_B > highest_awaiting_demand_for_product_B:
                        highest_awaiting_demand_for_product_B = instantenous_demand_for_product_B
                    if inventory_level_for_product_A > highest_inventory_level_for_product_A:
                        highest_inventory_level_for_product_A = inventory_level_for_product_A
                    if inventory_level_for_product_B > highest_inventory_level_for_product_B:
                        highest_inventory_level_for_product_B = inventory_level_for_product_B
                    previous_event_time = current_time
                    current_time = next_event_time

                    current_process = next_event




            for i in range(10):
                df = df.append({'Time': "-", 'Current Event': "-", 'Next Event Type': "-",
                                'Next Event Time':"-",
                                'Instantenous Demand for Product A':"-",
                                'Instantenous Demand for Product B':"-",
                                'Inventory Level for product A': "-",
                                'Inventory Level for product B':"-",
                                'Cumulative Demand For Product A':"-",
                                'Cumulative Demand For Product B':"-"}, ignore_index=True) 



            current_time = end_time_of_cycle_parts[k*4+1]     
            current_process = "-"
            next_event = "-"

            next_production_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_production_parameter * 60) )
            while current_time < end_time_of_cycle_parts[k*4+2]:
                    if inventory_level_for_product_B >= (order_up_to_level_for_B-1):
                        next_production_time_for_B = add_time_and_adjust(next_event_time, 1000 )
                        order_up_to_level_situation_for_B = 1 
                    if inventory_level_for_product_B < (order_up_to_level_for_B-1):
                        if next_event == "-" and k == 0:
                            next_production_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_production_parameter * 60) )
                        if next_event ==  "Production of B":
                            next_production_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_production_parameter * 60) )
                        if order_up_to_level_situation_for_B ==1:
                            next_production_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_production_parameter * 60) )
                            order_up_to_level_situation_for_B = 0 
                    if next_event == "Demand of A":
                        next_demand_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_demand_parameter * 60) )
                    if next_event == "Demand of B":
                        next_demand_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_demand_parameter * 60) )
                    
                    if next_production_time_for_B < next_demand_time_for_A and next_production_time_for_B< next_demand_time_for_B:
                        if next_production_time_for_B < end_time_of_cycle_parts[k*4+2]:
                            next_event = "Production of B"
                            next_event_time = next_production_time_for_B
                        else: 
                            next_event = "Setup for production of A"
                            next_event_time = end_time_of_cycle_parts[k*4+2]
                    
                    if next_demand_time_for_A < next_production_time_for_B and next_demand_time_for_A< next_demand_time_for_B:
                        if next_demand_time_for_A < end_time_of_cycle_parts[k*4+2]:
                            next_event = "Demand of A"
                            next_event_time = next_demand_time_for_A
                        else: 
                            next_event = "Setup for production of A"
                            next_event_time = end_time_of_cycle_parts[k*4+2]

                    if next_demand_time_for_B < next_demand_time_for_A and next_demand_time_for_B< next_production_time_for_B:
                        if next_demand_time_for_B < end_time_of_cycle_parts[k*4+2]:
                            next_event = "Demand of B"
                            next_event_time = next_demand_time_for_B
                        else: 
                            next_event = "Setup for production of A"
                            next_event_time = end_time_of_cycle_parts[k*4+2]

                    total_back_order_cost_for_A =  total_back_order_cost_for_A + (back_order_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_A)
                    total_back_order_cost_for_B = total_back_order_cost_for_B +(back_order_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_B)
                    total_back_order_cost = total_back_order_cost_for_A + total_back_order_cost_for_B
                    total_holding_cost_for_product_A = total_holding_cost_for_product_A + (holding_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_A)
                    total_holding_cost_for_product_B = total_holding_cost_for_product_B + (holding_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_B)
                    total_holding_cost = total_holding_cost_for_product_A + total_holding_cost_for_product_B

                    if current_time < end_time_of_cycle_parts[k*4+2]: 
                        if current_process == "Production of B":
                            inventory_level_for_product_B = inventory_level_for_product_B + 1 
                        if current_process == "Demand of A":
                            instantenous_demand_for_product_A = instantenous_demand_for_product_A +1 
                            cumulative_demand_for_product_A = cumulative_demand_for_product_A+1
                            if inventory_level_for_product_A > 0:
                                number_of_customer_request_met_immediately_for_A  = number_of_customer_request_met_immediately_for_A + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_A = number_of_customer_request_met_subsequently_for_A + 1 
                        if current_process == "Demand of B":
                            instantenous_demand_for_product_B =instantenous_demand_for_product_B + 1 
                            cumulative_demand_for_product_B = cumulative_demand_for_product_B+1
                            if inventory_level_for_product_B > 0:
                                number_of_customer_request_met_immediately_for_B  = number_of_customer_request_met_immediately_for_B + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_B = number_of_customer_request_met_subsequently_for_B + 1 

                    if instantenous_demand_for_product_A >= inventory_level_for_product_A:
                        instantenous_demand_for_product_A = instantenous_demand_for_product_A-inventory_level_for_product_A
                        inventory_level_for_product_A = 0
                    else:

                        inventory_level_for_product_A = inventory_level_for_product_A - instantenous_demand_for_product_A
                        instantenous_demand_for_product_A = 0

                    if instantenous_demand_for_product_B >= inventory_level_for_product_B:
                        instantenous_demand_for_product_B = instantenous_demand_for_product_B-inventory_level_for_product_B
                        inventory_level_for_product_B = 0
                    else:
                        inventory_level_for_product_B = inventory_level_for_product_B - instantenous_demand_for_product_B
                        instantenous_demand_for_product_B = 0


                    

                    df = df.append({'Time': current_time, 'Current Event': current_process, 'Next Event Type': next_event,
                                    'Next Event Time': next_event_time,
                                    'Instantenous Demand for Product A':instantenous_demand_for_product_A,
                                    'Instantenous Demand for Product B':instantenous_demand_for_product_B,
                                    'Inventory Level for product A': inventory_level_for_product_A,
                                    'Inventory Level for product B':inventory_level_for_product_B,
                                    'Total Holding Cost':total_holding_cost,
                                    'Total Backorder Cost':total_back_order_cost,
                                    'Total Setup Cost':total_setup_cost,
                                    'Total Cost': (total_setup_cost+total_holding_cost+total_back_order_cost),
                                    'Cumulative Demand For Product A':cumulative_demand_for_product_A,
                                    'Cumulative Demand For Product B':cumulative_demand_for_product_B}, ignore_index=True) 
                    if instantenous_demand_for_product_A > highest_awaiting_demand_for_product_A:
                        highest_awaiting_demand_for_product_A = instantenous_demand_for_product_A 
                    if instantenous_demand_for_product_B > highest_awaiting_demand_for_product_B:
                        highest_awaiting_demand_for_product_B = instantenous_demand_for_product_B
                    if inventory_level_for_product_A > highest_inventory_level_for_product_A:
                        highest_inventory_level_for_product_A = inventory_level_for_product_A
                    if inventory_level_for_product_B > highest_inventory_level_for_product_B:
                        highest_inventory_level_for_product_B = inventory_level_for_product_B
                    previous_event_time = current_time
                    current_time = next_event_time

                    current_process = next_event




            for i in range(10):
                df = df.append({'Time': "-", 'Current Event': "-", 'Next Event Type': "-",
                                'Next Event Time':"-",
                                'Instantenous Demand for Product A':"-",
                                'Instantenous Demand for Product B':"-",
                                'Inventory Level for product A': "-",
                                'Inventory Level for product B':"-",
                                'Cumulative Demand For Product A':"-",
                                'Cumulative Demand For Product B':"-"}, ignore_index=True) 



            current_time = end_time_of_cycle_parts[k*4+2]   
            current_process = "-"
            next_event = "-"
            total_setup_cost = total_setup_cost + setup_cost_for_B_to_A

            while current_time < end_time_of_cycle_parts[k*4+3] :
                    if next_event ==  "Demand of A":
                        next_demand_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_demand_parameter * 60) )
                    if next_event ==  "Demand of B":
                        next_demand_time_for_B = add_time_and_adjust(current_time, np.random.exponential(scale=1 /B_demand_parameter * 60) )
                    
                    
                    if  next_demand_time_for_A< next_demand_time_for_B:
                        if next_demand_time_for_A < end_time_of_cycle_parts[k*4+3]:
                            next_event = "Demand of A"
                            next_event_time = next_demand_time_for_A
                        else: 
                            next_event = "Production of A"
                            next_event_time = end_time_of_cycle_parts[k*4+3]

                    if next_demand_time_for_B < next_demand_time_for_A :
                        if next_demand_time_for_B < end_time_of_cycle_parts[k*4+3]:
                            next_event = "Demand of B"
                            next_event_time = next_demand_time_for_B
                        else: 
                            next_event = "Production of A"
                            next_event_time = end_time_of_cycle_parts[k*4+3]

                    total_back_order_cost_for_A =  total_back_order_cost_for_A + (back_order_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_A)
                    total_back_order_cost_for_B = total_back_order_cost_for_B +(back_order_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*instantenous_demand_for_product_B)
                    total_back_order_cost = total_back_order_cost_for_A + total_back_order_cost_for_B
                    total_holding_cost_for_product_A = total_holding_cost_for_product_A + (holding_cost_for_A*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_A)
                    total_holding_cost_for_product_B = total_holding_cost_for_product_B + (holding_cost_for_B*calculate_minutes_difference(current_time,previous_event_time)*inventory_level_for_product_B)
                    total_holding_cost = total_holding_cost_for_product_A + total_holding_cost_for_product_B


                    if current_time < end_time_of_cycle_parts[k*4+3]: 
                        if current_process == "Demand of A":
                            instantenous_demand_for_product_A = instantenous_demand_for_product_A +1 
                            cumulative_demand_for_product_A = cumulative_demand_for_product_A+1
                            if inventory_level_for_product_A > 0:
                                number_of_customer_request_met_immediately_for_A  = number_of_customer_request_met_immediately_for_A + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_A = number_of_customer_request_met_subsequently_for_A + 1 
                        if current_process == "Demand of B":
                            instantenous_demand_for_product_B =instantenous_demand_for_product_B + 1 
                            cumulative_demand_for_product_B = cumulative_demand_for_product_B+1
                            if inventory_level_for_product_B > 0:
                                number_of_customer_request_met_immediately_for_B  = number_of_customer_request_met_immediately_for_B + 1 
                            else:
                                number_of_customer_request_met_subsequently_for_B = number_of_customer_request_met_subsequently_for_B + 1 



                    if instantenous_demand_for_product_A >= inventory_level_for_product_A:
                        instantenous_demand_for_product_A = instantenous_demand_for_product_A-inventory_level_for_product_A
                        inventory_level_for_product_A = 0
                    else:

                        inventory_level_for_product_A = inventory_level_for_product_A - instantenous_demand_for_product_A
                        instantenous_demand_for_product_A = 0

                    if instantenous_demand_for_product_B >= inventory_level_for_product_B:
                        instantenous_demand_for_product_B = instantenous_demand_for_product_B-inventory_level_for_product_B
                        inventory_level_for_product_B = 0
                    else:
                        inventory_level_for_product_B = inventory_level_for_product_B - instantenous_demand_for_product_B
                        instantenous_demand_for_product_B = 0






                    df = df.append({'Time': current_time, 'Current Event': current_process, 'Next Event Type': next_event,
                                    'Next Event Time': next_event_time,
                                    'Instantenous Demand for Product A':instantenous_demand_for_product_A,
                                    'Instantenous Demand for Product B':instantenous_demand_for_product_B,
                                    'Inventory Level for product A': inventory_level_for_product_A,
                                    'Inventory Level for product B':inventory_level_for_product_B,
                                    'Total Holding Cost':total_holding_cost,
                                    'Total Backorder Cost':total_back_order_cost,
                                    'Total Setup Cost':total_setup_cost,
                                    'Total Cost': (total_setup_cost+total_holding_cost+total_back_order_cost),
                                    'Cumulative Demand For Product A':cumulative_demand_for_product_A,
                                    'Cumulative Demand For Product B':cumulative_demand_for_product_B}, ignore_index=True) 
                    if instantenous_demand_for_product_A > highest_awaiting_demand_for_product_A:
                        highest_awaiting_demand_for_product_A = instantenous_demand_for_product_A 
                    if instantenous_demand_for_product_B > highest_awaiting_demand_for_product_B:
                        highest_awaiting_demand_for_product_B = instantenous_demand_for_product_B
                    if inventory_level_for_product_A > highest_inventory_level_for_product_A:
                        highest_inventory_level_for_product_A = inventory_level_for_product_A
                    if inventory_level_for_product_B > highest_inventory_level_for_product_B:
                        highest_inventory_level_for_product_B = inventory_level_for_product_B
                    previous_event_time = current_time
                    current_time = next_event_time

                    current_process = next_event

            next_production_time_for_A = add_time_and_adjust(current_time, np.random.exponential(scale=1 /A_production_parameter * 60) )
            current_time = end_time_of_cycle_parts[k*4+3]     
            current_process = "-"
            next_event = "-"

            for i in range(10):
                df = df.append({'Time': "-", 'Current Event': "-", 'Next Event Type': "-",
                                'Next Event Time':"-",
                                'Instantenous Demand for Product A':"-",
                                'Instantenous Demand for Product B':"-",
                                'Inventory Level for product A': "-",
                                'Inventory Level for product B':"-",
                                'Cumulative Demand For Product A':"-",
                                'Cumulative Demand For Product B':"-"}, ignore_index=True) 

            cycle_average_cost_list.append((total_setup_cost+total_holding_cost+total_back_order_cost-total_cost_in_the_cycle_start)/calculate_minutes_difference(current_time,cycle_start_time))

            total_cost_in_the_cycle_start = total_setup_cost+total_holding_cost+total_back_order_cost
            cycle_start_time = current_time 

            if len(cycle_average_cost_list) >10:
                if (sum(cycle_average_cost_list)/len(cycle_average_cost_list))*0.2 > statistics.stdev(cycle_average_cost_list):
                    if k > 10:
                        simulation_continue = False

            
    average_inventory_level_for_product_A = ((total_holding_cost_for_product_A/holding_cost_for_A)/calculate_minutes_difference(current_time,starting_time))
    average_inventory_level_for_product_B = ((total_holding_cost_for_product_B/holding_cost_for_B)/calculate_minutes_difference(current_time,starting_time))
    average_awaiting_demand_for_product_A = ((total_back_order_cost_for_A/back_order_cost_for_A)/calculate_minutes_difference(current_time,starting_time))
    average_awaiting_demand_for_product_B = ((total_back_order_cost_for_B/back_order_cost_for_B)/calculate_minutes_difference(current_time,starting_time))
    total_cost = (total_setup_cost+total_holding_cost+total_back_order_cost)

    #return number_of_customer_request_met_immediately_for_A, number_of_customer_request_met_subsequently_for_A, number_of_customer_request_met_immediately_for_B,number_of_customer_request_met_subsequently_for_B,average_inventory_level_for_product_A, average_inventory_level_for_product_B, average_awaiting_demand_for_product_A,average_awaiting_demand_for_product_B,  highest_inventory_level_for_product_A, highest_inventory_level_for_product_B,highest_awaiting_demand_for_product_A,highest_awaiting_demand_for_product_B,total_cost, total_back_order_cost,total_holding_cost,total_setup_cost
    return total_cost/calculate_minutes_difference(current_time,starting_time),(number_of_customer_request_met_immediately_for_A+number_of_customer_request_met_immediately_for_B)/(number_of_customer_request_met_immediately_for_A+number_of_customer_request_met_immediately_for_B+number_of_customer_request_met_subsequently_for_A+number_of_customer_request_met_subsequently_for_B)





df = pd.read_excel("C:\\Users\\Kaan Ertan\\Desktop\\experiment_table_.xlsx")

# for i in range(len(df)):

for i in range(0,5):
    simulation_1 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1*"],df.loc[i,"S_2*"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under deterministic model"] = simulation_1[0]
    df.loc[i,"Percentage of customer request met immediately for deterministic model"] = simulation_1[1]
    simulation_2 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=0.9"],df.loc[i,"S_2* according to Heuristic with z=0.9"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 0.9"]= simulation_2[0]
    df.loc[i,"Cost per time under Heuristic with z = 0.9"] = simulation_2[1]
    simulation_3 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=1.65"],df.loc[i,"S_2* according to Heuristic with z=1.65"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 1.65"]= simulation_3[0]
    df.loc[i,"Percentage of customer request met immediately for z = 1.65"] = simulation_3[1]
    simulation_4 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=0"],df.loc[i,"S_2* according to Heuristic with z=0"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 0"]= simulation_4[0]
    df.loc[i,"Percentage of customer request met immediately for z = 0"] = simulation_4[1]
    simulation_5 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=0.5"],df.loc[i,"S_2* according to Heuristic with z=0.5"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 0.5"]= simulation_5[0]
    df.loc[i,"Percentage of customer request met immediately for z = 0.5"] = simulation_5[1]
    simulation_6 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=1.29"],df.loc[i,"S_2* according to Heuristic with z=1.29"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 1.29"]= simulation_6[0]
    df.loc[i,"Percentage of customer request met immediately for z = 1.29"] = simulation_6[1]
    simulation_7 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z=1"],df.loc[i,"S_2* according to Heuristic with z=1"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z = 1"]= simulation_7[0]
    df.loc[i,"Percentage of customer request met immediately for z = 1"] = simulation_7[1]
    simulation_8 = simulation_model(df.loc[i,"h_1"],df.loc[i,"b_1"],df.loc[i,"K"],df.loc[i,"h_2"],df.loc[i,"b_2"],df.loc[i,"K"],[df.loc[i,"T_1*"],df.loc[i,"T_2*"]],df.loc[i,"S_1* according to Heuristic with z formula"],df.loc[i,"S_2* according to Heuristic with z formula"],df.loc[i,"mu_1"],df.loc[i,"mu_2"],df.loc[i,"a_2"],df.loc[i,"a_1"],df.loc[i,"lambda_1"],df.loc[i,"lambda_2"])
    df.loc[i,"Cost per time under Heuristic with z formula"]= simulation_8[0]
    df.loc[i,"Percentage of customer request met immediately for z formula"] = simulation_8[1]
    print(i)

df.to_excel('experiment_table_last_version.xlsx', index=False)  
print("Finish")

