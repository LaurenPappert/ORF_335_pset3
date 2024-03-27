# -*- coding: utf-8 -*-
"""LPappert_ORF335_pset3.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZscaelPIbIrB2w-8mv0swglSXymFPQ_j
"""

def knapsack(C, W):
    n = len(C)
    # Sort the items in descending order of their value-to-weight ratio
    C.sort(key=lambda x: x[0]/x[1], reverse=True)
    # Initialize the dp array
    dp = [0] * (W + 1)
    for i, (value, weight) in enumerate(C):
        for j in range(W, weight - 1, -1):
            # If the weight of the current item is less than or equal to j,
            # we can choose to include it in the optimal solution
            dp[j] = max(dp[j], dp[j - weight] + value)
    # Return the maximum value that can be obtained with a weight limit of W
    return dp[W]

# Question 1a

C = [(2, 3), (3, 4), (4, 5), (5, 2), (10, 3), (40, 8), (15, 7), (25, 4)]
W = 12
print("x(C,W)=", knapsack(C, W))  # Output: 65

#Question 1d
# Get input from user
C_input = input("Enter pairs of (value, weight) separated by a space, and press Enter to finish: ").strip()
C_str_list = [x.strip() for x in C_input.split("),")]
C = [tuple(map(int, x.replace("(", "").replace(")", "").split(","))) for x in C_str_list if x]

W = int(input("Enter the weight limit: "))

# Compute x(C,W) using knapsack function from part a
print("x(C,W)=", knapsack(C, W))

#Question 2a
import math
import numpy as np
def american_put_option(S0, T, sigma, r, K, n):
  h = T / n
  r_n = math. exp(r * h) - 1
  u_n = math. exp(sigma * math. sqrt (h) )# Up factor
  d_n = 1 / u_n # Down factor
  p = (1 + r_n - d_n) / (u_n - d_n) # Risk-neutral probability P
  V = np.zeros ((n + 1, n + 1)) # initialize 2D array full of zeores
  for i in range(n + 1):
    ST = S0 * (u_n ** i) * (d_n ** (n - i)) # Stock price at node
    V[n, i] = max(K - ST, 0) # Payoff for put option

  for j in reversed (range(n)):
    for i in range(j + 1):
      S = S0 * (u_n ** i) * (d_n ** (j - i)) # Calculate stock price at node
      exercise = max(K - S, 0) # value if we exercise the option
      hold = (1/(1+r_n)) * (p*V[j+1, i+1]+(1-p)*V[j+1, i]) # value if we do not exercise the option
      V[j, i] = max (exercise, hold)
  # fill with maximum of exercising and holding
  return V[0, 0]

# Question 2b
S0 = 5150
T = 1/4
sigma = 0.1524
r = 0.0475
K = 5200
n = 500


american_put_price = american_put_option(S0, T, sigma, r, K, n)
print("The initial American put option price is: $", round(american_put_price, 2))

import math
import numpy as np

def binomial_tree_price(S0, sigma, r, T, n, K, B):
    h = T / n
    r_n = math.exp(r * h) - 1
    u_n = math.exp(sigma * math.sqrt(h))
    d_n = 1 / u_n
    p = (1 + r_n - d_n) / (u_n - d_n)

    S = np.zeros((n + 1, n + 1))
    V = np.zeros((n + 1, n + 1))

    for i in range(n + 1):
        for j in range(i + 1):
            S[i, j] = S0 * (u_n ** j) * (d_n ** (i - j))

    for j in range(n + 1):
        if S[n, j] >= K and S[n, j] > B:
            V[n, j] = 1

    for i in reversed(range(1, n + 1)):
        for j in range(i):
            if S[i - 1, j] > B:
                V[i - 1, j] = (p * V[i, j] + (1 - p) * V[i, j + 1]) / (1 + r_n)

    return V[0, 0]

# Parameters
params = [(200, 5200, 4900), (500, 5200, 4900), (1000, 5200, 4900)]

# Print option prices
for i, (n, K, B) in enumerate(params, ord('a')):
    option_price = binomial_tree_price(5150, 0.1524, 0.0475, 0.25, n, K, B)
    print(f"{chr(i)} . Number of time steps: {n}, Option price: ${option_price:.2f}\n")