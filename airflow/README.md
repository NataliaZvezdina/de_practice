### Overview

The main purpose is to create ETL solution using AirFlow through the API ([Rick and Morty API](https://rickandmortyapi.com/documentation/#location)) 
to find the three locations of the series with the most number of inhabitants.

---

### Tasks

1. Create a table in GreenPlum with fields `id`, `name`, `type`, `dimension`, `resident_cnt`.


2. With help of API ([Rick and Morty API](https://rickandmortyapi.com/documentation/#location)) find the three locations 
of the series with the most number of residents.


3. Write the values of the corresponding fields of these three locations in the table. `resident_cnt` - list length in 
`residents` field.


4. It is preferable to use the operator you wrote to compute the top-3 locations from the API.


5. You can either use `XCom` to transfer values between tasks or record the values immediately.


6. Remember to process the rerun of each task: prevent the table from being created again, make sure there are no 
duplicates in the table.
