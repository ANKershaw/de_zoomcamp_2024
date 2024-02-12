
#### Question 1: What is the sum of the outputs of the generator for limit = 5?
- **A**: 10.23433234744176
- **B**: 7.892332347441762
- **C**: **8.382332347441762 <- answer**
- **D**: 9.123332347441762
```Python
def square_root_generator(limit):

    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 5
generator = square_root_generator(limit)

sum_total = 0 
for sqrt_value in generator:
    sum_total += sqrt_value
    print(sum_total)
```

Output <p>
`
1.0
2.414213562373095
4.146264369941973
6.146264369941973
8.382332347441762
`

#### Question 2: What is the 13th number yielded by the generator?
- **A**: 4.236551275463989
- **B**: **3.605551275463989 <- answer**
- **C**: 2.345551275463989
- **D**: 5.678551275463989
```Python
def square_root_generator(limit):

    n = 1
    while n <= limit:
        yield n ** 0.5
        n += 1

# Example usage:
limit = 13
generator = square_root_generator(limit)

for sqrt_value in generator:
    print(sqrt_value)

```

Output: <p>
`
1.0
1.4142135623730951
1.7320508075688772
2.0
2.23606797749979
2.449489742783178
2.6457513110645907
2.8284271247461903
3.0
3.1622776601683795
3.3166247903554
3.4641016151377544
3.605551275463989`

#### Question 3: Append the 2 generators. After correctly appending the data, calculate the sum of all ages of people.
- **A**: **353 <- answer**
- **B**: 365
- **C**: 378
- **D**: 390

Refer to [python code](question_3.py) for answer.

#### Question 4: Merge the 2 generators using the ID column. Calculate the sum of ages of all the people loaded as described above.
- **A**: 215
- **B**: **266 <- answer**
- **C**: 241
- **D**: 258

Refer to [python code](question_4.py) for answer.
