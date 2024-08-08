#!/bin/bash

# Разделение IP-адреса на октеты
ip_address=$1
IFS='.' read -r -a octet_array <<< "$ip_address"

# Функция для перевода десятичного числа в двоичный формат
convert_to_binary() {
    number=$1
    binary_representation=""
    while [ $number -ne 0 ]; do
        binary_digit=$((number % 2))
        binary_representation="$binary_digit$binary_representation"
        number=$((number / 2))
    done
    
    # Добавляем ведущие нули, чтобы получить 8-битное представление
    while [ ${#binary_representation} -lt 8 ]; do
        binary_representation="0$binary_representation"
    done
    
    echo "$binary_representation"
}

# Преобразование каждого октета и вывод результата
binary_ip=""
#${octet_array[@]} разыменовывает массив и возвращает все его элементы не как одну строку
for octet in "${octet_array[@]}"; do
    binary_octet=$(convert_to_binary $octet)
    if [ -z "$binary_ip" ]; then
        binary_ip="$binary_octet"
    else
        binary_ip="$binary_ip.$binary_octet"
    fi
done

echo "$binary_ip"

