class KeyValueStore:
    def __init__(self):
        self.store = {}

    def add(self, key, value):
        self.store[key] = value

    def remove(self, key):
        if key in self.store:
            del self.store[key]
        else:
            print(f"Key '{key}' not found.")

    def find(self, key):
        if key in self.store:
            print(f"Value for key '{key}': {self.store[key]}")
        else:
            print(f"Key '{key}' not found.")

def process_operations(data):
    kv_store = KeyValueStore()
    for operation in data:
        if operation.startswith('+'):
            key, value = operation[1:].split('=')
            kv_store.add(key.strip(), value.strip())
        elif operation.startswith('-'):
            key = operation[1:].strip()
            kv_store.remove(key)
        elif operation.startswith('?'):
            key = operation[1:].strip()
            kv_store.find(key)

def run_tests():
    # Тест на добавление, поиск и удаление элемента
    data = [
        "+name=John",
        "?name",
        "+age=30",
        "?age",
        "-name",
        "?name"
    ]
    print("Test 1:")
    process_operations(data)

    # Тест на поиск несуществующего элемента
    data = [
        "?city",
        "+city=New York",
        "?city"
    ]
    print("\nTest 2:")
    process_operations(data)

    # Тест на добавление существующего ключа
    data = [
        "+name=John",
        "?name",
        "+name=Jane",
        "?name"
    ]
    print("\nTest 3:")
    process_operations(data)

    # Тест на удаление несуществующего ключа
    data = [
        "-city"
    ]
    print("\nTest 4:")
    process_operations(data)

    # Тест на работу с пустым набором данных
    data = []
    print("\nTest 5:")
    process_operations(data)

if __name__ == "__main__":
    run_tests()

