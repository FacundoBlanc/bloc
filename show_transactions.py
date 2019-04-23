#!/usr/bin/env python3
"""
NO PUDE IMPLEMENTAR DE MANERA CORRECTA LA FUNCION --add
"""

import argparse
from web3 import Web3
from web3.auto import w3
from web3.middleware import geth_poa_middleware
w3.middleware_stack.inject(geth_poa_middleware, layer=0)  # web3.exceptions.ValidationError: The field extraData is 97 bytes, but should be 32. .. .
from graphviz import Digraph

def searchTransactions(firstBlock, lastBlock, addresses, shortt, formatt, add):
    #firstBlock = 1240590
    g = Digraph('G', filename='transfer')
    if(lastBlock == 'latest'):          #si viene latest, convierto lastBlock a el ultimo bloque en curso
        lastBlock = w3.eth.blockNumber
    booe = True
    direcc = addresses
    for i in range(int(firstBlock), int(lastBlock)):    #Comienzo a recorrer los bloques elegidos
        tx = w3.eth.getBlock(i,booe)                #Recibo la informacion de cada bloque
        for diccionario in tx['transactions']:      #Obtengo el campo de las transacciones del bloque anteriormente mencionado
            try:
                if(diccionario['value'] > 0):       #Verifico que se haya hecho alguna transaccion de mas de un wei
                    labe = str(w3.fromWei(diccionario['value'],'ether'))+' ether  (' + str(i) +')'      #label que usaré en el graph
                    if not direcc:       #Si no elijo direcciones
                        # ~ if(add):
                            # ~ direcc.append(diccionario['from'])
                            # ~ direcc.append(diccionario['to'])
                        if(shortt):          #si lo necesito acortado
                            if(formatt == 'graphviz'):
                                g.node(diccionario['from'][2:10],diccionario['from'][2:10])
                                g.node(diccionario['to'][2:10],diccionario['to'][2:10])
                                g.edge(diccionario['from'][2:10], diccionario['to'][2:10], label=labe)
                            else:
                                print(diccionario['from'][2:10], " -> ", diccionario['to'][2:10], ": ", diccionario['value'] , "wei   Block ->: ", i)
                        else:
                            if(formatt == 'graphviz'):
                                g.node(diccionario['from'],diccionario['from'])
                                g.node(diccionario['to'],diccionario['to'])
                                g.edge(diccionario['from'], diccionario['to'], label=labe)
                            else:
                                print(diccionario['from'], " -> ", diccionario['to'], ": ", diccionario['value'] , "wei   Block ->: ", i)
                        
                    else:
                        for adArray in direcc:       #si elijo direcciones a buscar
                            if(adArray == diccionario['from'] or adArray == diccionario['to']):  #Verifico que pueda estár entre las direcciones que mandaron o recibieron transacciones
                                if(add):
                                    if(adArray != diccionario['from']):
                                        direcc.append(diccionario['from'])
                                    elif(adArray != diccionario['to']):
                                        direcc.append(diccionario['to'])
                                if(shortt):
                                    if(formatt == 'graphviz'):
                                        g.node(diccionario['from'][2:10],diccionario['from'][2:10])
                                        g.node(diccionario['to'][2:10],diccionario['to'][2:10])
                                        g.edge(diccionario['from'][2:10], diccionario['to'][2:10], label=labe)
                                    else:
                                        print(diccionario['from'][2:10], " -> ", diccionario['to'][2:10], ": ", diccionario['value'] , "wei   Block ->: ", i)
                                else:
                                    if(formatt == 'graphviz'):
                                        g.node(diccionario['from'],diccionario['from'])
                                        g.node(diccionario['to'],diccionario['to'])
                                        g.edge(diccionario['from'], diccionario['to'], label=labe)
                                    else:
                                        print(diccionario['from'], " -> ", diccionario['to'], ": ", diccionario['value'] , "wei   Block ->: ", i)
            except:
                raise Exception("no hay bloques que hayan hecho transacciones")
    if(formatt == 'graphviz'):
        print(g.source)
        g.view()


def block(bl):
    try:
        if(bl != 'latest'):
            val = int(bl)
            if (val >= 0):
                return bl
            raise Exception
        else:
            return bl
    except:
        raise argparse.ArgumentTypeError("Invalid type of block")  

def address(x):
    """Verifica si su argumento tiene forma de dirección ethereum válida"""
    try:
        if x[:2] == '0x':
            b = bytes.fromhex(x[2:])
            if len(b) == 20:
                return x
        raise Exception
    except:
        raise argparse.ArgumentTypeError("INvalid address")

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--addresses", metavar="ADDRESS", type=address, nargs='*')
    parser.add_argument("--add",help="Agrega las direcciones encontradas a la búsqueda", action="store_true", default=False)
    parser.add_argument("--firstBlock", "-f", help="Primer bloque del rango en el cual buscar", type=block, default=0)
    parser.add_argument("--lastBlock", "-l", help="Último bloque del rango en el cual buscar", type=block, default="latest")
    parser.add_argument("--format", help="Formato de salida", choices=["plain","graphviz"], default="plain")
    parser.add_argument("--short", help="Trunca las direcciones a los 8 primeros caracteres", action="store_true", default=False)
    args = parser.parse_args()
    searchTransactions(args.firstBlock,args.lastBlock,args.addresses,args.short, args.format, args.add)
