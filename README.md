# codecov-status

Github Action that check codecov status, replacing the need for CodeCov App

To use this action just include a step in a job that runs after all uploads
already happened:

```
    - name: Check codecov.io status
      uses: coactions/codecov-status@main
```

Be sure that this runs only on pull requests, otherwise will fail.
