import pandas as pd

def main_parser():
    # Считываем файл в строку
    with open('input_test.txt', 'r') as f:
        data = f.readlines()
    # Создаем списки для хранения чисел по каждой колонке
    column_1 = []
    column_2 = []
    # Пробегаемся по списку и добавляем элементы в соответствующие списки
    for i in range(1,len(data),7):
        phone = data[i]
        phone = phone[phone.find(" ")+1:]
        column_1.append(phone)
        column_2.append(data[i+4])
    # Создаем датафрейм
    df = pd.DataFrame({'phone': column_1, 'text': column_2})

    return df

##### отладка #####

#df = main_parser()
#print(df)
