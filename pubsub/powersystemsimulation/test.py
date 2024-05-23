import pypsa
import pandas as pd
import numpy as np
network = pypsa.Network()

network.add("Bus", "Bus_0", v_nom=20, v_mag_pu_set=1.02)
network.add("Bus", "Bus_1", v_nom=0.4)
network.add("Bus", "Bus_2", v_nom=0.4)
network.add("Carrier", "wind")
network.add(
    "Transformer",
    "Transformer_5",
    type="0.4 MVA 20/0.4 kV",
    bus0="Bus_0",
    bus1="Bus_1",
)
network.add(
    "Line", "LV line", type="NAYY 4x50 SE", bus0="Bus_1", bus1="Bus_2", length=0.1
)
network.add(
    "Generator", "Gen_0", bus="Bus_0",
    p_set=60,
    control="PV"
)
network.add("Load", "LV load", bus="Bus_2", p_set=0.1, q_set=0.05)


def run_pf(required_type):
    network.lpf()
    network.pf(use_seed=True)
    # output= pd.DataFrame(
    #     {
    #         "Voltage Angles": network.buses_t.v_ang.loc["now"] * 180.0 / np.pi,
    #         "Volate Magnitude": network.buses_t.v_mag_pu.loc["now"],
    #     }
    # )
    #gen=network.generators_t
    gen_attributes=process_gen(network)
    #bus_p=network.buses_t.p["Bus_0"]["now"]
    #col=network.buses_t.p.columns
    bus_attributes=process_bus(network)
    line_attributes=process_lines(network)
    load_attributes=process_load(network)
    transformer_attributes= process_transformer(network)
    if required_type=="network":
        result=network_info(gen_attributes,bus_attributes,line_attributes,load_attributes,transformer_attributes)
        return result
    if required_type=="iec61850":
        result=iec61850_info(gen_attributes,bus_attributes,line_attributes,load_attributes,transformer_attributes)
        return result
    #v_mag_pu
    #v_ang
    #q
    #print(network.transformers_t)
    #for g in network.lines_t.p0.columns:
    #p0
    #q0
    #p1
    #q1
    #print(network.buses_t)
    #print(network.loads_t)
    #q_set
    #p
    #q
    print()

def process_bus(network):
    bus_attributes={}
    for g in network.buses_t.p.columns:
        bus_attributes[str(g)+"_p"]=network.buses_t.p[g]["now"]
    for g in network.buses_t.q.columns:
        bus_attributes[str(g)+"_q"]=network.buses_t.p[g]["now"]
    for g in network.buses_t.v_mag_pu.columns:
        bus_attributes[str(g)+"_vMagPu"]=network.buses_t.p[g]["now"]
    for g in network.buses_t.v_ang.columns:
        bus_attributes[str(g)+"_vAng"]=network.buses_t.p[g]["now"]
    return bus_attributes

def process_gen(network):
    gen_attributes={}
    gen_attributes["Gen_0_P"]=network.generators_t.p["Gen_0"]["now"]
    gen_attributes["Gen_0_Q"]=network.generators_t.q["Gen_0"]["now"]
    return gen_attributes

def process_load(network):
    load_attributes={}
    for g in network.loads_t.q_set.columns:
        load_attributes[str(g)+"qSet"]=network.loads_t.q_set[g]["now"]
    for g in network.loads_t.p.columns:
        load_attributes[str(g)+"_p"]=network.loads_t.p[g]["now"]
    for g in network.loads_t.q.columns:
        load_attributes[str(g)+"_q"]=network.loads_t.q[g]["now"]
    return load_attributes

def process_lines(network):
    lines_attributes={}
    for g in network.lines_t.p0.columns:
        lines_attributes[str(g)+"_p0"]=network.lines_t.p0[g]["now"]
    for g in network.lines_t.q0.columns:
        lines_attributes[str(g)+"_q0"]=network.lines_t.q0[g]["now"]
    for g in network.lines_t.p1.columns:
        lines_attributes[str(g)+"_p1"]=network.lines_t.p1[g]["now"]
    for g in network.lines_t.q1.columns:
        lines_attributes[str(g)+"_q1"]=network.lines_t.q1[g]["now"]
    return lines_attributes

def process_transformer(network):
    transformer_attributes={}
    for g in network.transformers_t.p0.columns:
        transformer_attributes[str(g)+"_p0"]=network.transformers_t.p0[g]["now"]
    for g in network.transformers_t.q0.columns:
        transformer_attributes[str(g)+"_q0"]=network.transformers_t.q0[g]["now"]
    for g in network.transformers_t.p1.columns:
        transformer_attributes[str(g)+"_p1"]=network.transformers_t.p1[g]["now"]
    for g in network.transformers_t.q1.columns:
        transformer_attributes[str(g)+"_q1"]=network.transformers_t.q1[g]["now"]
    return transformer_attributes

def network_info(gen_attributes,bus_attributes,line_attributes,load_attributes,transformer_attributes):
    master_dict=dict()
    for key,value in gen_attributes.items():
        master_dict[key]=value
    for key,value in bus_attributes.items():
        master_dict[key]=value
    for key,value in line_attributes.items():
        master_dict[key]=value
    for key,value in load_attributes.items():
        master_dict[key]=value
    for key,value in transformer_attributes.items():
        master_dict[key]=value
    return master_dict
    
def iec61850_info(gen_attributes,bus_attributes,line_attributes,load_attributes,transformer_attributes):
    master_dict=dict()
    for key,value in gen_attributes.items():
        master_dict[key.replace('_','.')]=value
    for key,value in bus_attributes.items():
        master_dict[key.replace('_','.')]=value
    for key,value in line_attributes.items():
        master_dict[key.replace('_','.')]=value
    for key,value in load_attributes.items():
        master_dict[key.replace('_','.')]=value
    for key,value in transformer_attributes.items():
        master_dict[key.replace('_','.')]=value
    return master_dict
    pass
def info_61850():
    pass
if __name__=="__main__":
    run_pf("iec61850")