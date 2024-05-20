# codecov-status

Github Action that check codecov status, replacing the need for CodeCov App

To use this action just include a step in a job that runs after all uploads
already happened:

```yaml
    - name: Check codecov.io status
      if: github.event_name == 'pull_request'
      uses: coactions/codecov-status@main
```

If you want to see a full example of it being used in production, check
[this](https://github.com/ansible/ansible-dev-tools/blob/main/.github/workflows/tox.yml#L104-L106).
