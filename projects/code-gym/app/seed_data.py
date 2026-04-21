"""
Seed data: 50 curated LeetCode problems from top tech companies.
Difficulty, topics, companies, importance score (1-10), and pattern hint.
"""

PROBLEMS = [
    # ── ARRAYS ─────────────────────────────────────────────────────────────────
    {
        "title": "Two Sum",
        "slug": "two-sum",
        "difficulty": "Easy",
        "topics": "arrays,binary-search",
        "companies": "Google,Apple,Amazon,Meta,Microsoft",
        "importance": 10,
        "leetcode_number": 1,
        "pattern_hint": "Hash map for O(1) lookup",
        "description": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target."
    },
    {
        "title": "Best Time to Buy and Sell Stock",
        "slug": "best-time-to-buy-and-sell-stock",
        "difficulty": "Easy",
        "topics": "arrays,greedy",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 121,
        "pattern_hint": "Single pass, track min price so far",
        "description": "You want to maximize profit by choosing a single day to buy and a future day to sell."
    },
    {
        "title": "Contains Duplicate",
        "slug": "contains-duplicate",
        "difficulty": "Easy",
        "topics": "arrays,sorting",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 7,
        "leetcode_number": 217,
        "pattern_hint": "Set for O(1) lookup",
        "description": "Given an integer array nums, return True if any value appears at least twice in the array."
    },
    {
        "title": "Product of Array Except Self",
        "slug": "product-of-array-except-self",
        "difficulty": "Medium",
        "topics": "arrays",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 9,
        "leetcode_number": 238,
        "pattern_hint": "Prefix and suffix products",
        "description": "Return an array where each element is the product of all other elements."
    },
    {
        "title": "Maximum Subarray",
        "slug": "maximum-subarray",
        "difficulty": "Medium",
        "topics": "arrays,dynamic-programming",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 53,
        "pattern_hint": "Kadane's algorithm",
        "description": "Find the contiguous subarray with the largest sum."
    },
    {
        "title": "Container With Most Water",
        "slug": "container-with-most-water",
        "difficulty": "Medium",
        "topics": "arrays,greedy,two-pointers",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 11,
        "pattern_hint": "Two pointers, shrink from shorter side",
        "description": "Given n lines with heights, find two lines that with the x-axis form a container holding the most water."
    },
    {
        "title": "Merge Intervals",
        "slug": "merge-intervals",
        "difficulty": "Medium",
        "topics": "arrays,sorting",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 56,
        "pattern_hint": "Sort by start time, then merge",
        "description": "Merge all overlapping intervals."
    },
    {
        "title": "3Sum",
        "slug": "3sum",
        "difficulty": "Medium",
        "topics": "arrays,two-pointers",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 15,
        "pattern_hint": "Sort + two pointers, skip duplicates",
        "description": "Find all unique triplets that sum to zero."
    },
    {
        "title": "Subarray Sum Equals K",
        "slug": "subarray-sum-equals-k",
        "difficulty": "Medium",
        "topics": "arrays,hash-map",
        "companies": "Google,Amazon,Meta",
        "importance": 8,
        "leetcode_number": 560,
        "pattern_hint": "Prefix sum hash map",
        "description": "Find the number of contiguous subarrays that sum to k."
    },
    {
        "title": "Find All Duplicates in an Array",
        "slug": "find-all-duplicates-in-an-array",
        "difficulty": "Medium",
        "topics": "arrays",
        "companies": "Amazon,Microsoft",
        "importance": 6,
        "leetcode_number": 442,
        "pattern_hint": "Mark visited with negation",
        "description": "Find all elements that appear twice in an array where elements are in [1,n]."
    },
    # ── STRINGS ────────────────────────────────────────────────────────────────
    {
        "title": "Valid Anagram",
        "slug": "valid-anagram",
        "difficulty": "Easy",
        "topics": "strings,sorting,hash-map",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 242,
        "pattern_hint": "Character frequency count",
        "description": "Given two strings s and t, return True if t is an anagram of s."
    },
    {
        "title": "Longest Substring Without Repeating Characters",
        "slug": "longest-substring-without-repeating-characters",
        "difficulty": "Medium",
        "topics": "strings,sliding-window,two-pointers",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 3,
        "pattern_hint": "Sliding window with set/map",
        "description": "Find the length of the longest substring without repeating characters."
    },
    {
        "title": "Longest Palindromic Substring",
        "slug": "longest-palindromic-substring",
        "difficulty": "Medium",
        "topics": "strings,dynamic-programming,two-pointers",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 5,
        "pattern_hint": "Expand from center",
        "description": "Find the longest palindromic substring in s."
    },
    {
        "title": "Group Anagrams",
        "slug": "group-anagrams",
        "difficulty": "Medium",
        "topics": "strings,sorting,hash-map",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 49,
        "pattern_hint": "Sorted string as key",
        "description": "Group anagrams together."
    },
    {
        "title": "Minimum Window Substring",
        "slug": "minimum-window-substring",
        "difficulty": "Hard",
        "topics": "strings,sliding-window,hash-map",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 76,
        "pattern_hint": "Sliding window with counter",
        "description": "Find the smallest window in s that contains all characters of t."
    },
    # ── LINKED LISTS ──────────────────────────────────────────────────────────
    {
        "title": "Reverse Linked List",
        "slug": "reverse-linked-list",
        "difficulty": "Easy",
        "topics": "linked-lists,recursion",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 206,
        "pattern_hint": "Iterative: prev/current/next. Recursive: tail recursion",
        "description": "Reverse a singly linked list."
    },
    {
        "title": "Merge Two Sorted Lists",
        "slug": "merge-two-sorted-lists",
        "difficulty": "Easy",
        "topics": "linked-lists",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 21,
        "pattern_hint": "Dummy node + iteration",
        "description": "Merge two sorted linked lists into one sorted list."
    },
    {
        "title": "Linked List Cycle II",
        "slug": "linked-list-cycle-ii",
        "difficulty": "Medium",
        "topics": "linked-lists,two-pointers",
        "companies": "Google,Amazon,Meta",
        "importance": 8,
        "leetcode_number": 142,
        "pattern_hint": "Floyd's cycle detection",
        "description": "Given a linked list, return the node where the cycle begins."
    },
    {
        "title": "Remove Nth Node From End of List",
        "slug": "remove-nth-node-from-end-of-list",
        "difficulty": "Medium",
        "topics": "linked-lists,two-pointers",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 19,
        "pattern_hint": "Two pointers, one dummy",
        "description": "Remove the nth node from the end of a linked list."
    },
    {
        "title": "Add Two Numbers",
        "slug": "add-two-numbers",
        "difficulty": "Medium",
        "topics": "linked-lists,math",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 9,
        "leetcode_number": 2,
        "pattern_hint": "Digit-by-digit addition with carry",
        "description": "Add two numbers represented as linked lists (digits in reverse order)."
    },
    # ── TREES ─────────────────────────────────────────────────────────────────
    {
        "title": "Maximum Depth of Binary Tree",
        "slug": "maximum-depth-of-binary-tree",
        "difficulty": "Easy",
        "topics": "trees,recursion,bfs",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 104,
        "pattern_hint": "DFS (max depth) or BFS (level count)",
        "description": "Return the maximum depth of a binary tree."
    },
    {
        "title": "Invert Binary Tree",
        "slug": "invert-binary-tree",
        "difficulty": "Easy",
        "topics": "trees,recursion,bfs",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 226,
        "pattern_hint": "Swap children recursively",
        "description": "Invert a binary tree."
    },
    {
        "title": "Validate Binary Search Tree",
        "slug": "validate-binary-search-tree",
        "difficulty": "Medium",
        "topics": "trees,recursion",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 98,
        "pattern_hint": "Track min/max per subtree",
        "description": "Determine if a binary tree is a valid BST."
    },
    {
        "title": "Binary Tree Level Order Traversal",
        "slug": "binary-tree-level-order-traversal",
        "difficulty": "Medium",
        "topics": "trees,bfs",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 102,
        "pattern_hint": "BFS with queue, track levels",
        "description": "Return the level order traversal of binary tree node values."
    },
    {
        "title": "Lowest Common Ancestor of BST",
        "slug": "lowest-common-ancestor-of-a-binary-search-tree",
        "difficulty": "Medium",
        "topics": "trees,bst",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 235,
        "pattern_hint": "BST property: navigate left/right based on values",
        "description": "Find LCA in a BST."
    },
    {
        "title": "Serialize and Deserialize Binary Tree",
        "slug": "serialize-and-deserialize-binary-tree",
        "difficulty": "Hard",
        "topics": "trees,design,bfs",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 297,
        "pattern_hint": "Preorder + null markers, or BFS + queue",
        "description": "Encode and decode a binary tree."
    },
    {
        "title": "Binary Tree Right Side View",
        "slug": "binary-tree-right-side-view",
        "difficulty": "Medium",
        "topics": "trees,bfs,dfs",
        "companies": "Google,Amazon,Microsoft",
        "importance": 7,
        "leetcode_number": 199,
        "pattern_hint": "BFS: take rightmost per level",
        "description": "Return the nodes visible from the right side of the tree."
    },
    {
        "title": "Construct Binary Tree from Preorder and Inorder Traversal",
        "slug": "construct-binary-tree-from-preorder-and-inorder-traversal",
        "difficulty": "Medium",
        "topics": "trees,recursion",
        "companies": "Google,Amazon,Meta",
        "importance": 8,
        "leetcode_number": 105,
        "pattern_hint": "Root splits inorder at root index",
        "description": "Construct a binary tree from preorder and inorder traversals."
    },
    # ── GRAPHS ────────────────────────────────────────────────────────────────
    {
        "title": "Number of Islands",
        "slug": "number-of-islands",
        "difficulty": "Medium",
        "topics": "graphs,bfs,dfs,matrix",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 200,
        "pattern_hint": "DFS/BFS flood fill",
        "description": "Given a 2D grid, count the number of islands."
    },
    {
        "title": "Clone Graph",
        "slug": "clone-graph",
        "difficulty": "Medium",
        "topics": "graphs,bfs,dfs,hash-map",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 133,
        "pattern_hint": "BFS with visited map",
        "description": "Clone an undirected graph."
    },
    {
        "title": "Course Schedule",
        "slug": "course-schedule",
        "difficulty": "Medium",
        "topics": "graphs,dfs,bfs,topological-sort",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 207,
        "pattern_hint": "Topological sort (Kahn's or DFS cycle detection)",
        "description": "Determine if you can finish all courses given prerequisites."
    },
    {
        "title": "Word Ladder",
        "slug": "word-ladder",
        "difficulty": "Hard",
        "topics": "graphs,bfs",
        "companies": "Google,Amazon,Meta",
        "importance": 8,
        "leetcode_number": 127,
        "pattern_hint": "BFS with neighbor generation",
        "description": "Find the shortest transformation sequence from beginWord to endWord."
    },
    {
        "title": "Graph Valid Tree",
        "slug": "graph-valid-tree",
        "difficulty": "Medium",
        "topics": "graphs,bfs,dfs,union-find",
        "companies": "Google,Amazon,Meta",
        "importance": 7,
        "leetcode_number": 261,
        "pattern_hint": "n nodes, n-1 edges, no cycles = tree",
        "description": "Determine if the given edges form a valid tree."
    },
    # ── DYNAMIC PROGRAMMING ───────────────────────────────────────────────────
    {
        "title": "Climbing Stairs",
        "slug": "climbing-stairs",
        "difficulty": "Easy",
        "topics": "dynamic-programming",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 70,
        "pattern_hint": "Fibonacci pattern: dp[n] = dp[n-1] + dp[n-2]",
        "description": "You are climbing stairs. Each time you can climb 1 or 2 steps. How many distinct ways?"
    },
    {
        "title": "Coin Change",
        "slug": "coin-change",
        "difficulty": "Medium",
        "topics": "dynamic-programming,greedy",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 322,
        "pattern_hint": "Bottom-up DP: dp[i] = min(dp[i], dp[i-coin]+1)",
        "description": "Return the fewest coins needed to make up an amount."
    },
    {
        "title": "Longest Increasing Subsequence",
        "slug": "longest-increasing-subsequence",
        "difficulty": "Medium",
        "topics": "dynamic-programming,binary-search",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 300,
        "pattern_hint": "dp[i] = max(dp[j]+1) for j < i. Or binary search + patience sorting.",
        "description": "Find the length of the longest increasing subsequence."
    },
    {
        "title": "House Robber",
        "slug": "house-robber",
        "difficulty": "Medium",
        "topics": "dynamic-programming",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 198,
        "pattern_hint": "dp[i] = max(dp[i-1], dp[i-2] + nums[i])",
        "description": "You are a robber. Cannot rob two adjacent houses. Max loot?"
    },
    {
        "title": "Unique Paths",
        "slug": "unique-paths",
        "difficulty": "Medium",
        "topics": "dynamic-programming",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 62,
        "pattern_hint": "dp[i][j] = dp[i-1][j] + dp[i][j-1]",
        "description": "Robot in grid, can only move right or down. How many paths?"
    },
    {
        "title": "Longest Common Subsequence",
        "slug": "longest-common-subsequence",
        "difficulty": "Medium",
        "topics": "dynamic-programming",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 1143,
        "pattern_hint": "2D DP: if chars match, +1; else max of skipping one char from either string",
        "description": "Find the length of the longest common subsequence between two strings."
    },
    {
        "title": "Word Break",
        "slug": "word-break",
        "difficulty": "Medium",
        "topics": "dynamic-programming,hash-map",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 139,
        "pattern_hint": "dp[i] = any(dp[j] and s[j:i] in wordDict)",
        "description": "Given a string and a dictionary, can you break it into words?"
    },
    {
        "title": "Decode Ways",
        "slug": "decode-ways",
        "difficulty": "Medium",
        "topics": "dynamic-programming,strings",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 91,
        "pattern_hint": "dp[i] depends on s[i] and s[i-1:i+1]",
        "description": "Count the number of ways to decode a digit string."
    },
    {
        "title": "Palindromic Substrings",
        "slug": "palindromic-substrings",
        "difficulty": "Medium",
        "topics": "dynamic-programming,strings,two-pointers",
        "companies": "Google,Amazon,Meta",
        "importance": 7,
        "leetcode_number": 647,
        "pattern_hint": "Expand from center for each position",
        "description": "Count all palindromic substrings in a string."
    },
    {
        "title": "Edit Distance",
        "slug": "edit-distance",
        "difficulty": "Hard",
        "topics": "dynamic-programming,strings",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 72,
        "pattern_hint": "2D DP: dp[i][j] = min of replace/insert/delete operations",
        "description": "Min number of operations to convert word1 to word2."
    },
    # ── BINARY SEARCH ─────────────────────────────────────────────────────────
    {
        "title": "Binary Search",
        "slug": "binary-search",
        "difficulty": "Easy",
        "topics": "binary-search",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 704,
        "pattern_hint": "Classic: lo <= hi, mid, compare",
        "description": "Given a sorted array and a target, search for it."
    },
    {
        "title": "Search in Rotated Sorted Array",
        "slug": "search-in-rotated-sorted-array",
        "difficulty": "Medium",
        "topics": "binary-search",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 33,
        "pattern_hint": "Binary search with rotation check",
        "description": "Search in a rotated sorted array (no duplicates)."
    },
    {
        "title": "Find Minimum in Rotated Sorted Array",
        "slug": "find-minimum-in-rotated-sorted-array",
        "difficulty": "Medium",
        "topics": "binary-search",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 153,
        "pattern_hint": "Binary search, find the pivot",
        "description": "Find the minimum element in a rotated sorted array."
    },
    {
        "title": "Median of Two Sorted Arrays",
        "slug": "median-of-two-sorted-arrays",
        "difficulty": "Hard",
        "topics": "binary-search",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 10,
        "leetcode_number": 4,
        "pattern_hint": "Binary search on the smaller array to find partition",
        "description": "Find the median of two sorted arrays."
    },
    # ── HEAPS & SORTING ───────────────────────────────────────────────────────
    {
        "title": "Kth Largest Element in an Array",
        "slug": "kth-largest-element-in-an-array",
        "difficulty": "Medium",
        "topics": "heaps,sorting,quickselect",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 215,
        "pattern_hint": "Min-heap of size k, or quickselect",
        "description": "Find the kth largest element in an unsorted array."
    },
    {
        "title": "Merge K Sorted Lists",
        "slug": "merge-k-sorted-lists",
        "difficulty": "Hard",
        "topics": "heaps,linked-lists,divide-and-conquer",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 23,
        "pattern_hint": "Min-heap of k pointers",
        "description": "Merge k sorted linked lists into one sorted list."
    },
    {
        "title": "Top K Frequent Elements",
        "slug": "top-k-frequent-elements",
        "difficulty": "Medium",
        "topics": "heaps,hash-map,sorting",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 347,
        "pattern_hint": "Frequency map + min-heap of size k",
        "description": "Return the k most frequent elements."
    },
    # ── RECURSION & BACKTRACKING ─────────────────────────────────────────────
    {
        "title": "Permutations",
        "slug": "permutations",
        "difficulty": "Medium",
        "topics": "recursion,backtracking",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 46,
        "pattern_hint": "Swap + backtrack, or choose/uncheck",
        "description": "Return all permutations of an array."
    },
    {
        "title": "Subsets",
        "slug": "subsets",
        "difficulty": "Medium",
        "topics": "recursion,backtracking,bit-manipulation",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 78,
        "pattern_hint": "Include/exclude each element, or bit masks",
        "description": "Return all possible subsets of an array."
    },
    {
        "title": "Letter Combinations of a Phone Number",
        "slug": "letter-combinations-of-a-phone-number",
        "difficulty": "Medium",
        "topics": "recursion,backtracking",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 7,
        "leetcode_number": 17,
        "pattern_hint": "Digit → chars mapping, recursive combination",
        "description": "Given a digit string, return all possible letter combinations."
    },
    {
        "title": "N-Queens",
        "slug": "n-queens",
        "difficulty": "Hard",
        "topics": "recursion,backtracking",
        "companies": "Google,Amazon,Meta",
        "importance": 8,
        "leetcode_number": 51,
        "pattern_hint": "Track columns and diagonals with sets",
        "description": "Return all distinct solutions to the n-queens puzzle."
    },
    # ── STACKS & QUEUES ───────────────────────────────────────────────────────
    {
        "title": "Valid Parentheses",
        "slug": "valid-parentheses",
        "difficulty": "Easy",
        "topics": "stacks,strings",
        "companies": "Google,Amazon,Meta,Microsoft,Apple",
        "importance": 9,
        "leetcode_number": 20,
        "pattern_hint": "Stack: push open, pop on close, check mismatch",
        "description": "Given a string of brackets, check if it's valid."
    },
    {
        "title": "Min Stack",
        "slug": "min-stack",
        "difficulty": "Medium",
        "topics": "stacks,design",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 155,
        "pattern_hint": "Two stacks or one stack with (val, min) pairs",
        "description": "Design a stack that supports push, pop, top, and retrieving the min element."
    },
    {
        "title": "Evaluate Reverse Polish Notation",
        "slug": "evaluate-reverse-polish-notation",
        "difficulty": "Medium",
        "topics": "stacks",
        "companies": "Google,Amazon,Meta",
        "importance": 7,
        "leetcode_number": 150,
        "pattern_hint": "Stack: push numbers, pop and apply operator",
        "description": "Evaluate an expression in Reverse Polish Notation."
    },
    # ── TRIES ─────────────────────────────────────────────────────────────────
    {
        "title": "Implement Trie (Prefix Tree)",
        "slug": "implement-trie-prefix-tree",
        "difficulty": "Medium",
        "topics": "tries,design",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 9,
        "leetcode_number": 208,
        "pattern_hint": "Node with children dict and is_end flag",
        "description": "Implement a Trie with insert, search, and startsWith methods."
    },
    {
        "title": "Word Search II",
        "slug": "word-search-ii",
        "difficulty": "Hard",
        "topics": "tries,backtracking,dfs",
        "companies": "Google,Amazon,Meta,Microsoft",
        "importance": 8,
        "leetcode_number": 212,
        "pattern_hint": "Build Trie from words, DFS with backtracking",
        "description": "Given a 2D board and a list of words, find all words in the board."
    },
]
