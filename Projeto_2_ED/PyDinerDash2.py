# PyDinerDash 2
import os

print('=> restaurante aberto')

def sorting(dictionary):
    for k in sorted(dictionary):
        dictionary[k] = sorted(dictionary[k])

    return sorted(dictionary)
    
def update_tables(tables_configuration, areas):
    file = os.getcwd() + '/mesas/' + input()
    with open(file, 'r') as file:
        for table in file:
            table = table.strip('\n')
            table = table.split(', ')    
            tables_configuration[int(table[0])] = table[1:]
            if table[1] not in areas:
                areas.append(table[1])
       
    return tables_configuration, areas

def update_menu(menu):
    file = os.getcwd() + '/cardapio/' + input()
    with open(file, 'r') as file:
        for recipe in file:
            recipe = recipe.strip('\n')
            recipe = recipe.split(', ')
            menu[recipe[0]] = recipe[1::]
    return menu

def update_stock(stock):
    file = os.getcwd() + '/estoque/' + input()
    with open(file, 'r') as file:
        for ingredient in file:
            ingredient = ingredient.strip('\n')
            ingredient = ingredient.split(', ')
            if ingredient[0] in stock:
                stock[ingredient[0]] += int(ingredient[1])
            else:
                stock[ingredient[0]] = int(ingredient[1])    

    return stock

def tables_report(tables_configuration, areas):
    aux = {}
    for k in tables_configuration:
        for area in areas:
            if area in tables_configuration[k]:
                areas.remove(area)
    tables_configuration['empty_areas'].append(areas)

    if len(tables_configuration) < 2:
        print('- restaurante sem mesas')
    else:
        for k in tables_configuration:
            if k == 'empty_areas':
                if tables_configuration[k] != []:
                    for i in range(len(tables_configuration[k][0])):
                        aux[tables_configuration[k][0][i]] = 0
            elif tables_configuration[k][0] not in aux:
                aux[tables_configuration[k][0]] = [(k, tables_configuration[k][1])]
            elif tables_configuration[k][0] in aux:
                aux[tables_configuration[k][0]].append((k, tables_configuration[k][1]))
    for k in sorted(aux):
            print(f'area: {k}')
            if aux[k] == 0:
                print('- area sem mesas')            
            else:
                v = sorted(aux[k])
                for i in range(len(v)):
                    print(f'- mesa: {v[i][0]}, status: {v[i][1]}')

def menu_report(menu):
    aux = {}
    if menu == {}:
        print('- cardapio vazio')
    else:
        for k in menu:
            aux[k] = []
            for i in range(len(menu[k])):
                if menu[k][i] in aux[k]:
                    aux[k] = [(menu[k][i])]
                else:
                    aux[k].append(menu[k][i])
        for k in sorting(aux):   
            component = menu[k]
            print(f'item: {k}')
            for i in range(len(aux[k])):         
                print(f'- {aux[k][i]}: {component.count(aux[k][i])}')
    
def stock_report(stock):
    if stock == {}:
        print('- estoque vazio')
    else:
        for k in sorted(stock):
            print(f'{k}: {stock[k]}')

def make_order(tables_configuration, menu, stock):
    remove_stock = []
    order = input().split(', ')
    has_stock = True
    for k in menu:
        for i in range(len(menu[k])):
            if k == order[1] and menu[k][i] in stock:
                has_stock = True
            elif k != order[1]:
                break
            else:    
                has_stock = False
                break
        if has_stock == False:
            break

    if int(order[0]) not in tables_configuration:
        print(f'erro >> mesa {order[0]} inexistente')

    elif tables_configuration[int(order[0])][1] == 'livre':
        print(f'erro >> mesa {order[0]} desocupada')

    elif order[1] not in menu:
        print(f'erro >> item {order[1]} nao existe no cardapio')
    
    elif has_stock == False:
        print(f'erro >> ingredientes insuficientes para produzir o item {order[1]}')   

    else:
        print(f'sucesso >> pedido realizado: item {order[1]} para mesa {order[0]}')
        if int(order[0]) in order_history:
            order_history[int(order[0])].append(order[1])
        else:
            order_history[int(order[0])] = [order[1]]
        
        for i in range(len(menu[order[1]])):
            for k in stock:
                if menu[order[1]][i] == k:
                    stock[k] -= 1
        for k in stock:
            if stock[k] == 0:
                remove_stock.append(k)
        for ingredient in remove_stock:
            stock.pop(ingredient)

    return order_history, stock

def orders_report(order_history):
    if order_history == {}:
        print('- nenhum pedido foi realizado')
    else:
        for k in sorting(order_history):
            print(f'mesa: {k}')
            for i in range(len(order_history[k])):
                print(f'- {order_history[k][i]}')
                
def close_restaurant(order_history):
    if order_history == {}:
        print('- historico vazio')
    else:
        i = 1
        for k in (order_history):
            for j in range(len(order_history[k])):
                print(f'{i}. mesa {k} pediu {order_history[k][j]}')
                i += 1

    print('=> restaurante fechado')


command = ''
tables_configuration = {'empty_areas': []}
areas = []
menu = {}
stock = {}
order_history = {}
order = ''

while command != '+ fechar restaurante':
    command = input()
    if command == '+ atualizar mesas':
        update_tables(tables_configuration, areas)
    elif command == '+ atualizar cardapio':
        update_menu(menu)
    elif command == '+ atualizar estoque':
        update_stock(stock)
    elif command == '+ relatorio mesas':
        tables_report(tables_configuration, areas)
    elif command == '+ relatorio cardapio':
        menu_report(menu)
    elif command == '+ relatorio estoque':
        stock_report(stock)
    elif command == '+ fazer pedido':
        make_order(tables_configuration, menu, stock)
    elif command == '+ relatorio pedidos':
        orders_report(order_history)
    elif command == '+ fechar restaurante':
        close_restaurant(order_history)
    else:
        print('erro >> comando inexistente')


# python PyDinerDash2.py < test01.txt > result01.txt | python PyDinerDash2.py < test02.txt > result02.txt | python PyDinerDash2.py < test03.txt > result03.txt | python PyDinerDash2.py < test04.txt > result04.txt | python PyDinerDash2.py < test05.txt > result05.txt | python PyDinerDash2.py < test06.txt > result06.txt | python PyDinerDash2.py < test07.txt > result07.txt | python PyDinerDash2.py < test08.txt > result08.txt | python PyDinerDash2.py < test09.txt > result09.txt | python PyDinerDash2.py < test10.txt > result10.txt | python PyDinerDash2.py < test11.txt > result11.txt | python PyDinerDash2.py < test12.txt > result12.txt | python PyDinerDash2.py < test13.txt > result13.txt | python PyDinerDash2.py < test14.txt > result14.txt | python PyDinerDash2.py < test15.txt > result15.txt | python PyDinerDash2.py < test16.txt > result16.txt | python PyDinerDash2.py < test17.txt > result17.txt | python PyDinerDash2.py < test18.txt > result18.txt | python PyDinerDash2.py < test19.txt > result19.txt | python PyDinerDash2.py < test20.txt > result20.txt
