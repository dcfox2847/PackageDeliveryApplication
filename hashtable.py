class ChainingHashTable:

    # O(n)
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new item into hash table

    # O(1)
    def insert(self, key, item):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        bucket_list.append(item)

    # Searches for item with matching key, then returns the item if found / O(n)
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    # Removes item from the hash table if there is a key match / O(n)
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        if key in bucket_list:
            bucket_list.remove(key)

    # Returns all of the items from the hash table to a list for ease of sorting / O(n^2)
    def return_all_items(self, list_of_items):
        for bucket in self.table:
            for item in bucket:
                list_of_items.append(item)
