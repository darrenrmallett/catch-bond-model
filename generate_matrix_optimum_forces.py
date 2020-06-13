import sys, math

###################################################################################################

#variables. set the fixed values here.
k1_UR = 6.1
k2_UR = 78
k1_sens = -2.9
k2_sens = 5.4
k3_sens = 3.7
k4_sens = -2.1

def lifetime(force, k3_UR, k4_UR):
    
    k3_UR = float(k3_UR)
    k4_UR = float(k4_UR)
    
    k1 = k1_UR*math.exp(force/k1_sens)
    k2 = k2_UR*math.exp(force/k2_sens)
    k3 = k3_UR*math.exp(force/k3_sens)
    k4 = k4_UR*math.exp(force/k4_sens)
    
    t = (k1+k2+k4)/((k1*k4)+(k2*k3)+(k3*k4))
    
    return t

def biphasic( forces_and_lifetimes ):
    
    list_of_lifetimes = list(forces_and_lifetimes.values())
    this_biphasic = 0
    
    x = 0
    for value in list_of_lifetimes:  
        if (x == 1):
            change = value - prev_value
            
            if (change < 0) :
                sign = 'neg'
            else :
                sign = 'pos'
            
        elif (x >= 1) :
            
            change = value - prev_value
            
            if ((change < 0 and sign == 'neg') or (change > 0 and sign == 'pos')) :
                pass
            elif ((change < 0 and sign == 'pos') or (change < 0 and sign == 'pos')) :
                this_biphasic = 1
            
        x += 1            
        prev_value = value
        
    return this_biphasic

def optimal_force( forces_and_lifetimes ):
    #finds the force in a list of forces that has the highest lifetime.
    
    list_of_lifetimes = list(forces_and_lifetimes.values())
    list_of_forces = list(forces_and_lifetimes.keys())
    
    highest_peak = max(list_of_lifetimes)
    position = list_of_lifetimes.index(highest_peak)
    
    return list_of_forces[position]

###################################################################################################

k3_list = []
k4_list = []

for i in range(0, 301, 1):
    i_new = i
    k4_list.append(i_new)
    
for i in range(0, 251, 1):
    i_new = i/10
    k3_list.append(i_new)

k3_list = k3_list[1:]
k4_list = k4_list[1:]

forces_and_lifetimes = {}    
for i in range( 0, 81, 1 ):
    i_new = i/5
    forces_and_lifetimes[i_new] = 0
    
k3_k4_values = {}

forces = list(forces_and_lifetimes.keys())

for k4_UR in k4_list : 
    #for each k4 unloaded rate value...
    
    k4_UR_str = str(k4_UR)
    k3_k4_values[k4_UR_str] = {}
    
    for k3_UR in k3_list:
        #for each k3 unloaded rate value...
        
        list_of_lifetimes = []
        
        for force in forces:
            #for each force...
            
            #we want to get if this is biphasic or not...
            #put the lifetimes for this k3,k4 unloaded rate pair into a list
            #forces_and_lifetimes[force] = lifetime(force, k3_UR, k4_UR)
            life_time = lifetime(force, k3_UR, k4_UR)
            forces_and_lifetimes[force] = life_time
        
        o_f = optimal_force( forces_and_lifetimes )

        k3_UR_str = str(k3_UR) #just make it a string.
        
        #store the result of the score in a dictionary with keys corresponding to k4 and k3 unloaded rates.
        k3_k4_values[k4_UR_str][k3_UR_str] = o_f
        
#output separated by tabs in a way that can easily be copied and pasted into excel.
#edit the output header to reflect what the code is doing, to remind the user what the matrix is showing.

output = f'# Unloaded rates: k1: {k1_UR}; k2: {k2_UR}; k3 and k4 vary.\n'
output += f'# Sensitivities: k1: {k1_sens}; k2: {k2_sens}; k3: {k3_sens}; k4: {k4_sens}\n'
output += f'# This is using the MILLER WILD-TYPE DATA parameters!\n'
output += f'# Output: Is the curve biphasic? 1 = Biphasic; 0 = Not biphasic\n\n'

output += f'\t k3'
for k3_value in k3_list:
    output += f'\t {k3_value}'
output += f'\nk4\n'

for k4_value in k4_list:
    output += f'{k4_value}\t'
    k4_value = str(k4_value)
    for k3_key in k3_k4_values[k4_value]:
        output += f'\t{k3_k4_values[k4_value][k3_key]}'
    output += f'\n'
    
#change the name of the file if you want.
filehandle = open('Biphasic_binary_scores_MillerWT_vary_k3UR_and_k4UR_Stu2-AID_k4sensitivity_only.txt','w')
filehandle.write(output)
filehandle.close()

print('done')