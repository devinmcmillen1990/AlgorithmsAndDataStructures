<h1>1. Binary Search for a Final Height</h2>

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)

<h2>Idea</h2>

Keep two counters
1. ```needed``` - how many additional ```)``` characters the processed portion still needs
   - ```(``` -> ```needed += 2```
   - ```)``` -> ```needed -= 1``` 
2. <strong>insertions</strong> - how many characters we have inserted so far

The tricky part is hanlding an unfinished ```))``` pair before another ```(``` appears.

<h2>Code</h2>

```python
class Solution:

```

<h2>Time Complexity : </h2> 

<strong>O(n)</strong>, because each character is processed once

<h2>Space Complexity : </h2> 

<strong>O(1)</strong>, only counters are storing data

<h2>Categories</h2>

<ul>
    <li>Array</li>
    <li>Strings</li>
    <li>Greedy</li>
</ul>

[Back to Problem](../LC_2333_MinimumSumOfSquareDifferences.md)