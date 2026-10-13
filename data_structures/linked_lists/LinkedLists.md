# Linked lists — quick reference

Two independent, noncircular implementations with the same public API:
`LinkedList` (singly) and `DoublyLinkedList` (doubly). Python 3.10+; standard library only.

## Files and running

```text
linked_list/                 # Place under data_structures/ in your repository.
├── __init__.py
├── node.py                  # Node(value, next=None)
├── linkedlist.py            # LinkedList
├── doublynode.py            # DoublyNode(value, next=None, prev=None)
├── doublylinkedlist.py      # DoublyLinkedList
├── test_cases.json          # Shared input/output snapshots
├── tests.py                 # Shared tests + structure-specific checks
└── README.md
```

Keep your working singly implementation to test it; the supplied `linkedlist.py`
is a reference to compare/merge. Node constructors assign references; list
methods maintain reciprocal links.

```bash
# Inside this directory:
python3 tests.py
python3 tests.py TestSinglyLinkedList
python3 tests.py TestDoublyLinkedList
python3 tests.py TestDoublyLinkedList.test_json_snapshots

# Alternatively, from AlgorithmsAndDataStructures/:
python3 data_structures/linked_list/tests.py
python3 -m data_structures.linked_list.tests
```

Tests use the existing repository helper `utils.load_test_cases`; keep this folder
under `data_structures/`. The runner adds the repository root to `sys.path`.
Package mode requires the underscore spelling `data_structures`. When retaining
your own code, keep the conditional sibling imports for both execution modes.
Discovery: `python3 -m unittest discover -s data_structures/linked_list -p 'tests.py'`.

## Structure and invariants

```text
Singly: head -> [10] -> [20] -> [30] -> None
                                ^ tail

Doubly: None <- [10] <-> [20] <-> [30] -> None
                ^ head            ^ tail
```

Both store `_head`, `_tail`, `_size`. Empty: endpoints are `None`, size is zero.
Otherwise `tail.next is None`; doubly also requires `head.prev is None` and
`a.next.prev is a` for every non-tail node. Following only `next`/`prev` must
terminate. Both use **O(n)** storage; doubly adds one reference per node.

## Shared API contract

`index(value)` returns the **first index or `None`**; check `position is not None`,
not truthiness. `None` is a valid payload. `remove(value)` raises `ValueError` when
absent. `pop()` defaults to `-1` and returns a **value**, not a node. `reverse()`
returns a **new reversed shallow copy**: independent nodes, shared payload objects,
unchanged original. These `index`/`reverse` contracts differ from built-in lists.

Negative indices count from the end. `insert` inserts **before** a clamped position
in `[0,n]`, including empty lists. Other indexed operations require `[-n,n-1]`
or raise `IndexError`. Non-integers/slices raise `TypeError`; Boolean indices are
accepted as zero/one. Searches use identity **or** equality; duplicates and
unhashable values are allowed. Mutators return `None` except `pop` and `reverse`.

## Operations and costs

Examples start fresh with values `[10,20,30]`. `n` = length, `k` = appended count,
`R` = representation length. Costs describe **this code**, assuming constant-cost
value comparisons. Space includes new nodes/output, not existing payload objects.

| Operation | Effect / example | Singly time | Doubly time | Extra space |
|---|---|---:|---:|---:|
| `__init__(values)` | Build a new chain in input order | O(n) | O(n) | O(n) nodes |
| `prepend(5)` | Add at head → `[5,10,20,30]` | O(1) | O(1) | O(1) node |
| `append(40)` | Add at tail → `[10,20,30,40]` | O(1) | O(1) | O(1) node |
| `insert(1,15)` | Insert before index 1 → `[10,15,20,30]` | O(n) worst | O(n) worst | O(1) node |
| `extend([40,50])` | Append multiple values → `[10,20,30,40,50]` | O(k) | O(k) | O(k) nodes |
| `pop(0)` | Remove head; return `10` | O(1) | O(1) | O(1) |
| `pop()` / `pop(-1)` | Remove tail; return `30` | **O(n)** | **O(1)** | O(1) |
| `pop(i)` / `del L[i]` | Remove an indexed item; `del` discards the value | O(n) worst | O(n) worst | O(1) |
| `remove(20)` | Remove first match → `[10,30]` | O(n) worst | O(n) worst | O(1) |
| `index(20)` | First matching position → `1`; missing → `None` | O(n) worst | O(n) worst | O(1) |
| `count(20)` | Count matches → `1` | O(n) | O(n) | O(1) |
| `20 in L` (`__contains__`) | Membership → `True` | O(n) worst | O(n) worst | O(1) |
| `L[1]` (`__getitem__`) | Read value → `20` | O(n) worst | O(n) worst | O(1) |
| `L[1] = 99` (`__setitem__`) | Replace payload → `[10,99,30]`; keep node | O(n) worst | O(n) worst | O(1) |
| `len(L)` / `bool(L)` | Stored size / whether nonempty | O(1) | O(1) | O(1) |
| `for value in L` (`__iter__`) | Traverse `10,20,30`; no copying | O(n) total | O(n) total | O(1) |
| `list(L)` | Materialize values as a Python list | O(n) | O(n) | O(n) references |
| `L.reverse()` | New list `[30,20,10]`; original unchanged | O(n) | O(n) | O(n) nodes |
| `reversed(L)` | Backward iterator, not a new linked list | O(n²) total¹ | O(n) total | O(1) iterator |
| `clear()` | Detach all nodes → `[]` | O(n) | O(n) | O(1) |
| `repr(L)` (`__repr__`) | `LinkedList([...])` or `DoublyLinkedList([...])` | O(n+R) | O(n+R) | O(n+R) |

Insertion at either end is O(1). Reading/replacing either endpoint is also O(1)
here: singly `_node_at()` explicitly recognizes the tail. For a normalized
position `i`, doubly `_node_at()` starts at the nearer end and costs
**O(min(i+1, n-i))**; singly walks from the head except for its tail shortcut.
`_normalize_index()` is O(1) time/space; `_node_at()` uses O(1) working space.
`Node`/`DoublyNode` construction is O(1) time/space. `__delitem__` delegates to
`pop`; truthiness uses `__len__` (no separate `__bool__` needed).

¹ Singly has no `__reversed__`: Python falls back to repeated indexed access.
Doubly implements `__reversed__` by following `prev`.
[Python's reversal protocol](https://docs.python.org/3/reference/datamodel.html#object.__reversed__).

**Finding a node is not the same as relinking it.** Once the relevant node(s)
are known, changing a fixed number of links is O(1). Indexed lookup and
value-based search can still be O(n). Singly removing the tail needs its
predecessor; doubly already stores it. An O(1) LRU design needs a dictionary of
node references and direct node unlink/relink operations, not `remove(value)`.

## Link updates at a glance

```text
insert(1, 15):    10 <-> 20 <-> 30  becomes  10 <-> 15 <-> 20 <-> 30
                 previous=10, following=20, new=15
                 new.prev=previous; new.next=following
                 previous.next=new; following.prev=new

pop(1):          10 <-> 20 <-> 30  becomes  10 <-> 30; return 20
                 previous.next=following; following.prev=previous
                 removed.next=None; removed.prev=None
```

Singly performs the same **forward-link** changes, without `prev` assignments.
`prepend`/`append` are boundary cases; `pop` updates head/tail when needed.
`clear` repeats head removal. `reverse` builds an independent chain by prepending:
`10 → [10]`, `20 → [20,10]`, `30 → [30,20,10]`.

## Real applications

| Singly linked lists | Why links help |
|---|---|
| [Boost.Pool free lists](https://www.boost.org/doc/libs/latest/libs/pool/doc/html/boost_pool/pool/pooling.html) | Unused memory chunks link together; allocation/deallocation can take/return a chunk at the front. |
| [Clojure persistent lists](https://github.com/clojure/clojure/blob/clojure-1.12.0/src/jvm/clojure/lang/PersistentList.java) | Persistent singly linked sequences support adding a front element while sharing the old tail; unlike these classes, they are immutable. |
| [Windows interlocked SLists](https://learn.microsoft.com/en-us/windows/win32/sync/interlocked-singly-linked-lists) | Platform-provided atomic push/pop chains for concurrent applications; synchronization is essential and is **not** provided here. |

| Doubly linked lists | Why links help |
|---|---|
| [Linux kernel object lists](https://docs.kernel.org/core-api/list.html) | Intrusive circular lists support removing, moving, and splicing known entries; unlike our noncircular layout, they use a circular list head. |
| [LLVM instruction/basic-block lists](https://llvm.org/docs/ProgrammersManual.html#llvm-adt-ilist-h) | Intrusive `ilist` supports bidirectional traversal and moving compiler IR objects. |
| [CPython 3.13 LRU-cache Python fallback](https://github.com/python/cpython/blob/3.13/Lib/functools.py) | A dictionary and circular doubly linked recency chain support moving cached entries; CPython normally imports the optimized C wrapper. |

For ordinary Python queues/deques, consider
[`collections.deque`](https://docs.python.org/3/library/collections.html#collections.deque).
Linked nodes have allocation and locality costs; arrays can be a better fit for
scanning and random access ([Linux guidance](https://docs.kernel.org/core-api/list.html)).

## Practice — singly

| Problem | Difficulty | Focus |
|---|---|---|
| [206. Reverse Linked List](https://leetcode.com/problems/reverse-linked-list/) | Easy | Reverse existing links; aim for O(1) extra space, unlike our copying `reverse()`. |
| [21. Merge Two Sorted Lists](https://leetcode.com/problems/merge-two-sorted-lists/) | Easy | Dummy head, two cursors, reuse nodes. |
| [141. Linked List Cycle](https://leetcode.com/problems/linked-list-cycle/) | Easy | Slow/fast pointers; do not use ordinary traversal on a cyclic input. |
| [19. Remove Nth Node From End](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Medium | Pointer gap and head removal. |
| [143. Reorder List](https://leetcode.com/problems/reorder-list/) | Medium | Find middle, reverse a half, interleave. |
| [138. Copy List with Random Pointer](https://leetcode.com/problems/copy-list-with-random-pointer/) | Medium | Copy node relationships, including an extra arbitrary reference. |

## Practice — doubly / suitable doubly linked designs

| Problem | Difficulty | Focus |
|---|---|---|
| [Reverse a doubly linked list](https://www.hackerrank.com/challenges/reverse-a-doubly-linked-list/problem) | Easy | In-place reversal of both links; differs from our copying method. |
| [Sorted insertion in a doubly linked list](https://www.hackerrank.com/challenges/insert-a-node-into-a-sorted-doubly-linked-list/problem) | Easy | Maintain reciprocal links and endpoints. |
| [707. Design Linked List](https://leetcode.com/problems/design-linked-list/) | Medium | Implement either representation; platform API differs from this one. |
| [430. Flatten a Multilevel Doubly Linked List](https://leetcode.com/problems/flatten-a-multilevel-doubly-linked-list/) | Medium | Splice child chains and repair `prev`. |
| [1472. Design Browser History](https://leetcode.com/problems/design-browser-history/) | Medium | Bidirectional cursor; an array/stack design is also valid. |
| [146. LRU Cache](https://leetcode.com/problems/lru-cache/) · [NeetCode](https://neetcode.io/problems/lru-cache/question) | Medium | Dictionary → node lookup, O(1) unlink/relink; not indexed removal. |

Links are primary problem sources; suggested techniques are practice targets,
not mandatory implementations.

**Scope:** learning implementations, not thread-safe containers. No slicing,
value-based container equality, sorting, or public node-handle mutation API.
Avoid structural mutation during iteration. `L.extend(L)` snapshots the original
values using O(n) temporary references; **do not use** `L.extend(iter(L))` or a
self-referential generator. External iterables are streamed; an iterator error
partway through `extend` leaves already-appended values in place.