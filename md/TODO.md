# TODO

## Design

- Consider dividing the sorting algorithms into sub-categories, like comparison-based and integer sorting algorithms

## CI/CD

- Travis CI is no longer free. I need to find a free alternative.
- The scripts inside [`scripts`](../scripts) are a bit inflexible. For example, they return an error if the specific version of Python is not installed. We can probably get rid of them and simplify the way the algorithms can be test locally.
- It might also be a good idea to migrate from virtual environments to docker containers (optional)

## Testing

- See [`tests/README.md`](../tests/README.md)

## Next features

- Implement Radix Sort and Introsort
- Implement the Catmull-Rom spline