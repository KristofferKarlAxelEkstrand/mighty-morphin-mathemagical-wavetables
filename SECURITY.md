# Security Policy

## Supported Versions

We strive to support security updates for actively maintained versions.  
Older versions may not receive security patches.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We value the security of our users and contributors. If you've found a vulnerability:

- **Where to report:**  
  For sensitive security issues, please email **kristoffer.ekstrand@gmail.com**.
  For non-sensitive issues, open a new *issue* or start a *discussion* in the Security category.
- **Response Time:**  
  Because this project is maintained by volunteers, response times and patches may take up to **6 months**. We appreciate your patience and understanding!
- **DIY fixes welcome:**  
  Is your vulnerability something you can fix yourself? Fantastic! Feel free to submit a PR with your patch (especially since this whole project runs locally).
- **On acceptance/decline:**  
  We'll do our best to update you along the way. If fixes are accepted, they'll be merged and released in the next supported version update.

## Security Measures

This project implements several security best practices:

-  **Code Quality**: All code passes strict linting (pylint, flake8, mypy)
-  **Type Safety**: Complete type hints with strict mypy checking
-  **Testing**: 87%+ test coverage with comprehensive test suite
-  **Dependencies**: Automated dependency updates via Dependabot
-  **CI/CD**: Automated testing on all pull requests
-  **Input Validation**: All user inputs are validated before processing

## Security Considerations

### Audio File Generation
-  This project generates audio files (WAV format) which are safe for use
-  Generated files contain only mathematical waveform data
-  No executable code or scripts are embedded in generated files

### Dependencies
-  Minimal dependencies (numpy, soundfile)
-  All dependencies are actively maintained and regularly updated
-  Dependabot automatically checks for security vulnerabilities

### Data Privacy
-  This project does not collect, store, or transmit any user data
-  All processing happens locally on your machine
-  Generated wavetables are stored only in the specified output directory

Thank you for helping keep mighty-morphin-mathemagical-wavetables safe for everyone!
