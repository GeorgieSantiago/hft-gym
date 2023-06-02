## Trade Engine AI

##### Notes
**Action space**:
    for each symbol
    [
        [buy|sell|nothing] = -1 0 1 (sign of the first value)
        [percentage] = 1 - 100
    ]
    if buy get total amount possible to buy and place an order
    to buy a % of that

    if sell get the total amount held and place an order to sell
    the % of that

    Example action output
    ```
    [[ 1 83]
    [-1 67]
    [ 1 58]]
    ```

**Observation space**
    This uses the HOLC shape for each symbol

    example observation space
    ```
    [[729.42896  640.5956   196.64128  465.47382 ]
    [806.8653   191.71783  981.9553   578.2849  ]
    [513.8814   123.039116 548.7596   437.76187 ]
    [918.3371   657.2043   490.68494  721.82446 ]
    [298.56995  636.23193  377.30753  650.08466 ]]
    ```