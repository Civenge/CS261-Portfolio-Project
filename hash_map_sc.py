# Name: Kyle Greene
# OSU Email: greeneky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 12/2/2022
# Description: Implement a chaining Hash Map with the following methods: put(),
# empty_buckets(), table_load(), clear(), resize_table(), get(), contains_key(),
# remove(), get_keys_and_values(), and find_mode().


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Pass in a key:value pair, where the key is a string.  If the existing key already exists,
        update the associated value with the new value.  If the key doesn't exist, add the new
        key:value pair into the hash table.  The table must be resized to double the current
        capacity when the method is called and the load factor is greater or equal to 1.0.
        """
        # check if resize is needed
        if self.table_load() >= 1:
            self.resize_table(self._capacity * 2)

        # first run the key through the hash function get convert to an int
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the size of the DynamicArray
        modulo_value = self._capacity

        # find the index where the key will be inserted
        key_insert_index = key_value_unmodified % modulo_value

        # assign variable to track which bucket the value goes into
        bucket = self._buckets[key_insert_index]

        # verify if the linked list has the key already in it, returns the node if so
        node_contains = self.contains_key(key)

        # if key is present, update value
        if node_contains is True:

            # iterate through the existing DynamicArray in the Hash Map
            for index in range(self._capacity):

                # get the linked list to evaluate
                current_bucket = self._buckets.get_at_index(key_insert_index)

                # iterate through the linked list to get all the keys
                for node in current_bucket:
                    if node.key == key:
                        node.value = value

        # if key is not present, create a new node and update size of linked list
        else:
            bucket.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # initialize counter
        count = 0

        # iterate through the DynamicArray
        for index in range(self._buckets.length()):

            # check if the current index of DynamicArray is empty Linked List
            current_bucket = self._buckets.get_at_index(index)
            if current_bucket.length() == 0:
                count += 1

        return count

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # load factor equals total number of elements in the
        # table divided by total number of buckets

        return float(self._size/self._capacity)

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the
        underlying table capacity.
        """
        # create a new DynamicArray to replace the existing in our Hash Map
        self._buckets = DynamicArray()

        # fill the table with empty Linked Lists equal to the capacity of our Hash Map
        for index in range(self._capacity):
            self._buckets.append(LinkedList())

        # set our size of our Hash Map back to 0
        self._size = 0

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the hash table.  All existing key:value pairs must
        remain in the new hash map, and all hash table links must be rehashed.  If
        the new_capacity is less than 1, do nothing.  If the new_capacity is 1 or
        greater, verify it is a prime number.  If not, change it to the next prime
        number using _is_prime() and _next_prime() methods.
        """
        # verify new capacity is >= 1
        if new_capacity < 1:
            return

        # check if new capacity is prime, if not set to next prime number
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)

        # need to check if load factor is valid
        while (self._size/new_capacity) > 1:
            new_capacity = new_capacity * 2
            new_capacity = self._next_prime(new_capacity)

        # reset size to 0 to be updated below when each bucket is filled
        self._size = 0

        # create a storage DynamicArray to store the resized Hash Map
        storage_da = DynamicArray()

        # populate the new DynamicArray with empty Linked Lists
        for index in range(new_capacity):
            storage_da.append(LinkedList())

        # iterate through the existing DynamicArray to rehash each index
        for bucket in range(self._capacity):

            # remove the last element from the DynamicArray and set to variable
            current_bucket = self._buckets.pop()

            # iterate through the Linked List
            for node in current_bucket:

                # get the existing key and value from the old node
                key = node.key
                value = node.value

                # hash the key into the new DynamicArray
                new_key = self._hash_function(key) % new_capacity
                bucket = storage_da[new_key]

                # insert the new node into the new DynamicArray and update size
                bucket.insert(key, value)
                self._size += 1

        # reassign the Hash Map to use the new DynamicArray
        self._buckets = storage_da

        # update the capacity to the new capacity
        self._capacity = new_capacity

    def get(self, key: str):
        """
        Returns the value associated with the given key.  If the key is not in the
        hash map, return None.
        """
        # first get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value

        # iterate through the existing DynamicArray in the Hash Map
        for index in range(self._capacity):

            # get the linked list to evaluate
            current_bucket = self._buckets.get_at_index(insert_location)

            # iterate through the linked list to get all the keys
            for node in current_bucket:
                # if key found, return value
                if node.key == key:
                    return node.value

        # key not found, return None
        return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map, otherwise returns False.
        An empty hash map does not contain keys and should return False.
        """
        # edge case when there is an empty hash map, return False
        if self._size == 0:
            return False

        # first get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value

        # iterate through the existing DynamicArray in the Hash Map
        for index in range(self._capacity):

            # get the linked list to evaluate
            current_bucket = self._buckets.get_at_index(insert_location)

            # iterate through the linked list to get all the keys
            for node in current_bucket:
                # if key found, return True
                if node.key == key:
                    return True

        # key not found, return False
        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and associated value from the hash map.  If
        the key is not in the hash map, the method does nothing.
        """
        # first get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value

        # go to the correct linked list location
        bucket = self._buckets[insert_location]

        # remove the node, .remove returns false if node wasn't found
        remove = bucket.remove(key)

        # if True, there was a node found and removed, decrement size
        if remove is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a DynamicArray where each index contains a tuple of a
        (key, value) pair stored in the hash map.  The order does not
        matter.
        """
        # make a new DynamicArray to store all the (key, value) pairs
        key_value_pair = DynamicArray()

        # iterate through the existing DynamicArray in the Hash Map
        for index in range(self._capacity):

            # get the linked list to evaluate
            current_bucket = self._buckets.get_at_index(index)

            # iterate through the linked list to get all the keys
            for node in current_bucket:

                # append all the (key, value) pairs to the new DynamicArray
                key_value_pair.append((node.key, node.value))

        return key_value_pair


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Receives a DynamicArray (unsorted).  Return a tuple containing,
    in order, a DynamicArray comprising the mode value(s) of the array
    and an integer that represents the highest frequency.  If there are
    multiple values with the highest frequency, return all of them
    (order does not matter).
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    map = HashMap()

    # iterate through the DynamicArray that is passed in, adding it to the hash map
    for index in range(da.length()):

        # if the key already exists, increment the counter(value) for the key, then update the key
        if map.contains_key(da[index]):
            value = map.get(da[index])
            value += 1
            map.put(da[index], value)

        # if the key doesn't exist, insert the key with counter(value) of 1
        else:
            map.put(da[index], 1)

    # set mode to index 0 of DynamicArray, since we know the DA has at least 1 value
    count = 0

    # iterate through the DynamicArray, tracking what associated bucket has the highest value
    for bucket in range(da.length()):
        key = da.get_at_index(bucket)

        # check if the value of a particular key is greater than count
        if map.get(key) > count:

            # when a new highest value is found, update count
            count = map.get(key)

    # create an array to store all the final
    result = DynamicArray()

    # get a DynamicArray of all the keys and values
    entries = map.get_keys_and_values()

    # iterate through the Hash Map, when a value is found that matches our max count,
    # append to result DA
    for bucket in range(entries.length()):
        entry = entries.get_at_index(bucket)
        if entry[1] == count:
            result.append(entry[0])

    # return the tuple
    return result, count


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())

    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))

    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())

    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - resize example 2a")
    # print("----------------------")
    # m = HashMap(82, hash_function_2)
    # m.put("key25", "key25")
    # m.put("key72", "key72")
    # m.put("key4", "key4")
    # m.put("key502", "key502")
    # m.put("key520", "key520")
    # m.put("key620", "key620")
    # m.put("key173", "key173")
    # m.put("key471", "key471")
    # m.put("key357", "key357")
    # m.put("key396", "key396")
    # m.put("key669", "key669")
    # m.put("key978", "key978")
    # print(m.get_size(), m.get_capacity())
    #
    # m.resize_table(9)
    # print("size: ", m.get_size(), "capacity: ", m.get_capacity())
    # print("Expected result is: size: 12, capacity: 23")
    #
    # print("\nPDF - resize example 2b")
    # print("----------------------")
    # m = HashMap(52, hash_function_2)
    # m.put("key645", "key645")
    # m.put("key555", "key555")
    # m.put("key655", "key655")
    # m.put("key593", "key593")
    # m.put("key769", "key769")
    #
    # print(m.get_size(), m.get_capacity())
    #
    # m.resize_table(4)
    # print("size: ", m.get_size(), "capacity: ", m.get_capacity())
    # print("Expected result is: size: 5, capacity: 5")

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))

    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))

    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)

    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')

    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(2)
    # print(m.get_keys_and_values())

    # print("\nPDF - find_mode example 1")
    # print("-----------------------------")
    # da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    # mode, frequency = find_mode(da)
    # print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    # print("\nPDF - find_mode example 2")
    # print("-----------------------------")
    # test_cases = (
    #     ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
    #     ["one", "two", "three", "four", "five"],
    #     ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    # )
    #
    # for case in test_cases:
    #     da = DynamicArray(case)
    #     mode, frequency = find_mode(da)
    #     print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
