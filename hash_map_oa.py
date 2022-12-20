# Name: Kyle Greene
# OSU Email: greeneky@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6 - HashMap Implementation
# Due Date: 12/2/2022
# Description: Implement an open addressing Hash Map with the following methods:
# put(), table_load(), empty_buckets(), resize_table(), get(), contains_key(),
# remove(), clear(), get_keys_and_values(), __iter()__ and __next()__.

from a6_include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Updates the key/value pair in the hash map.
        If the given key already exists, the associated
        value must be replaced with the new value.  If the
        given key is not in the hash map, a new key/value
        pair is added.

        When the current load factor is >= 0.5, double
        the current capacity.
        """

        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)

        # hash the key
        hash_value = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = hash_value % modulo_value

        # get value at bucket to verify if None
        bucket = self._buckets[insert_location]

        # verify if the index already has the key in it
        if bucket is None:
            self._buckets[insert_location] = HashEntry(key, value)
            self._size += 1

        # verify the key is unique, if not update the value
        elif self._buckets[insert_location].key == key and self._buckets[insert_location].is_tombstone is False:
            self._buckets[insert_location].value = value

        # see if the key was a removed value, if so, make it valid and update size and tombstone
        elif self._buckets[insert_location].key == key and self._buckets[insert_location].is_tombstone is True:
            self._buckets[insert_location].value = value
            self._buckets[insert_location].is_tombstone = False
            self._size += 1

        else:
            # j is the variable to store the quadratic probing
            j = 1
            while bucket is not None:
                insert_location = (hash_value + (j ** 2)) % modulo_value
                bucket = self._buckets[insert_location]
                j += 1
                # check if duplicate key, if so continue
                if self._buckets[insert_location] is not None and self._buckets[insert_location].key == key:
                    # update value if no tombstone
                    if self._buckets[insert_location].is_tombstone is False:
                        self._buckets[insert_location].value = value
                        return
                    # check if the key is a tombstone
                    if self._buckets[insert_location].is_tombstone is True:
                        self._buckets[insert_location].value = value
                        self._buckets[insert_location].is_tombstone = False
                        self._size += 1
                        return

            # not a duplicate key, so create the new entry
            self._buckets[insert_location] = HashEntry(key, value)
            self._size += 1

    def table_load(self) -> float:
        """
        Returns the current hash table load factor.
        """
        # load factor equals total number of elements in the
        # table divided by total number of buckets

        return float(self._size / self._capacity)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table.
        """
        # initialize counter
        count = 0

        # iterate through the DynamicArray
        for index in range(self._buckets.length()):

            # check if the current index of DynamicArray is None
            current_bucket = self._buckets.get_at_index(index)
            if current_bucket is None:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """
        Changes the capacity of the internal hash table.
        All existing key/value pairs must remain, and all
        hash table links must be rehashed.

        If new_capacity is less than the current number of
        elements in the hash map, the method does nothing.

        If new_capacity is valid, make sure it is a prime
        number.  If not prime, change it to the next highest
        prime number using _is_prime() and _next_prime().
        """

        # verify new capacity at least as big as number of elements
        if new_capacity < self._size or new_capacity < 1:
            return

        # check if new capacity is prime, if not set to next prime number
        if not self._is_prime(new_capacity):
            new_capacity = self._next_prime(new_capacity)

        # create a new hash map to store the resized map
        new_map = HashMap(new_capacity, self._hash_function)

        # iterate through the old hash map to rehash the values
        for index in range(self._capacity):
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                new_map.put(self._buckets[index].key, self._buckets[index].value)

        # update capacity, buckets to match the new hash map
        self._capacity = new_map._capacity
        self._buckets = new_map._buckets

    def get(self, key: str) -> object:
        """
        Returns the value associated with a given key.  If a key
        is not in the hash map, return None.
        """
        # first get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value
        initial_location = insert_location
        probe = self._buckets.get_at_index(insert_location)

        if self._buckets[insert_location] is not None and self._buckets[insert_location].is_tombstone is False:
            if self._buckets[insert_location].key == key:
                return self._buckets[insert_location].value

            else:
                # probe being None means the key is not in the hash map
                j = 1
                while probe is not None:
                    insert_location = (initial_location + (j ** 2)) % modulo_value

                    # if a quadratic probe finds a duplicate key, update value
                    if probe.key == key and probe.is_tombstone is False:
                        return probe.value

                    # find next probe location and update probe variable
                    probe = self._buckets.get_at_index(insert_location)
                    j += 1

        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map,
        otherwise return False.  An empty hash map does
        not contain any keys.
        """
        # first check if the hash map is empty, return False
        if self._size == 0:
            return False

        # get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value
        initial_location = insert_location
        probe = self._buckets.get_at_index(insert_location)

        if self._buckets[insert_location] is not None and self._buckets[insert_location].is_tombstone is False:
            if self._buckets[insert_location].key == key:
                return True

            else:
                # probe being None means the key is not in the hash map
                j = 1
                while probe is not None:
                    insert_location = (initial_location + (j ** 2)) % modulo_value

                    # if a quadratic probe finds key, return value
                    if probe.key == key and probe.is_tombstone is False:
                        return True

                    # find next probe location and update probe variable
                    probe = self._buckets.get_at_index(insert_location)
                    j += 1

        return False

    def remove(self, key: str) -> None:
        """
        Removes the given key and its associated value from
        the hash map.  If the key is not in the hash map,
        the method does nothing.
        """
        # first check if the hash map is empty, return
        if self._size == 0:
            return

        # first get the key value
        key_value_unmodified = self._hash_function(key)

        # modulo is equal to the capacity of the hash table
        modulo_value = self._capacity

        # find the index of the insert location
        insert_location = key_value_unmodified % modulo_value

        # j stores the quadratic probing value
        j = 1

        # search for the key until we hit a None value, meaning the key is not in the hash map
        while self._buckets[insert_location] is not None:

            # if we find the key, decrement size and mark tombstone to True
            if self._buckets[insert_location].key == key and self._buckets[insert_location].is_tombstone is False:
                self._buckets[insert_location].is_tombstone = True
                self._size -= 1
                return

            # insert location has the quadratic probing
            insert_location = (key_value_unmodified + (j ** 2)) % self._capacity

            # increment quadratic probe to the next one
            j += 1

    def clear(self) -> None:
        """
        Clears the content of the hash map without changing
        the underlying hash table capacity.
        """
        # create a new DynamicArray to replace the existing in our Hash Map
        self._buckets = DynamicArray()

        # fill the table with None equal to the capacity of our Hash Map
        for index in range(self._capacity):
            self._buckets.append(None)

        # set our size of our Hash Map back to 0
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns a dynamic array where each index contains a
        tuple of a key/value pair stored in the hash map.
        Order does not matter.
        """
        # make a new DynamicArray to store all the (key, value) pairs
        key_value_pair = DynamicArray()

        # iterate through the existing DynamicArray in the hash map
        for index in range(self._capacity):

            # verify the hash map index has a value and it isn't a tombstone, if so append to DA
            if self._buckets[index] is not None and self._buckets[index].is_tombstone is False:
                key_value_pair.append((self._buckets[index].key, self._buckets[index].value))

        return key_value_pair

    def __iter__(self):
        """
        Enables the hash map to iterate across itself.
        """

        # set a variable to track the iterations
        self._index = 0
        return self

    def __next__(self):
        """
        Returns the next item in the hash map, based
        upon the current location of the iterator.
        """
        # create a try block that will return the next value or raise an
        # exception if none exist

        try:
            value = self._buckets[self._index]

        except Exception:
            raise StopIteration

        # while loop to skip over iterations when there is no valid key
        while value is None or value.is_tombstone is True:
            if self._index >= self._capacity - 1:
                # we have hit the end of the iteration, raise exception
                raise StopIteration
            self._index = self._index + 1
            value = self._buckets[self._index]

        # increment the pointer
        self._index = self._index + 1

        return value


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":
    #
    # print("\nPDF - put example 1")
    # print("-------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('str' + str(i), i * 100)
    #     if i % 25 == 24:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

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
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
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

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        if m.table_load() > 0.5:
            print(f"Check that the load factor is acceptable after the call to resize_table().\n"
                  f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
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
    # m = HashMap(11, hash_function_1)
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
    #
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
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())

    # print("\nPDF - __iter__(), __next__() example 1")
    # print("---------------------")
    # m = HashMap(10, hash_function_1)
    # for i in range(5):
    #     m.put(str(i), str(i * 10))
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
    #
    # print("\nPDF - __iter__(), __next__() example 2")
    # print("---------------------")
    # m = HashMap(10, hash_function_2)
    # for i in range(5):
    #     m.put(str(i), str(i * 24))
    # m.remove('0')
    # m.remove('4')
    # print(m)
    # for item in m:
    #     print('K:', item.key, 'V:', item.value)
