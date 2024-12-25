# Guardians - Phishing Website Protection

Guardians is a dedicated repository for tracking and recording phishing websites, specifically those targeting users of Suiet, our secure and user-friendly crypto wallet. By maintaining a comprehensive list of malicious websites, we aim to protect users from fraudulent activities and maintain the security and integrity of their digital assets.

## Introduction

Phishing attacks have become increasingly common in the world of cryptocurrencies. As the popularity of digital assets grows, so does the number of malicious actors looking to exploit unsuspecting users. Guardians aims to combat these threats by providing a continuously updated list of phishing websites targeting Suiet crypto wallet users.

## Files

### Block Lists
- coin-list.json: This file contains a block list for coin types. Entities listed here are subject to prefix matching for identification and management purposes.
- object-list.json: This file houses a block list for objects, including Non-Fungible Tokens (NFTs). Prefix matching principles are employed for effective identification and management of objects within projects.
- domain-list.json: Here you'll find a block list for domain names. Prefix matching is applied to identify and manage domains efficiently.

### Bloom Filters
For improved performance and reduced memory usage, we also provide Bloom filter versions of our block lists:

- coin-list.bloom.json: Bloom filter for coin types
- object-list.bloom.json: Bloom filter for objects
- domain-list.bloom.json: Bloom filter for domains
- package-list.bloom.json: Bloom filter for packages

Each Bloom filter file contains metadata about the filter configuration and the base64-encoded filter data. The Bloom filters are configured with a false positive rate of 0.1%.

## Accessing the Data

All content, including the block lists and Bloom filters, can be accessed directly via https://guardians.suiet.app:

- Block Lists:
  - https://guardians.suiet.app/coin-list.json
  - https://guardians.suiet.app/object-list.json
  - https://guardians.suiet.app/domain-list.json
  - https://guardians.suiet.app/package-list.json

- Bloom Filters:
  - https://guardians.suiet.app/coin-list.bloom.json
  - https://guardians.suiet.app/object-list.bloom.json
  - https://guardians.suiet.app/domain-list.bloom.json
  - https://guardians.suiet.app/package-list.bloom.json

To clone the repository, use the following command:

```shell
git clone https://github.com/your-username/your-repo.git
```

## How It Works

Guardians maintains a blocklist of known phishing websites targeting Suiet users. This blocklist is updated regularly to ensure that users are protected from the latest threats. When a user accesses a website through the Suiet wallet, the URL is checked against the list. If the URL is found on the list, the user is warned and redirected to a safe page.

For efficient lookups, we use Bloom filters - a space-efficient probabilistic data structure that allows for quick membership testing. While Bloom filters may occasionally produce false positives, they never produce false negatives, making them ideal for our security-focused application. Our Bloom filters are configured with a 0.1% false positive rate to maintain high accuracy while minimizing resource usage.

## Contributing

We encourage the community to contribute to the Guardians repository by reporting phishing websites and helping us keep the list up-to-date. To contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch with a descriptive name, e.g., add-phishing-site-xyz.
3. Add the malicious URL(s) to the list.json file.
4. Commit your changes and create a pull request.

Please provide as much information as possible about the phishing website, including screenshots and any relevant evidence. Our team will review your submission and, if accepted, will update the list accordingly.

You can also submit the data directly to the [form](https://forms.gle/z7TqNYsppWBoUEJP7), but only those who submit through GitHub may be eligible for incentive in the future. 

## License

Guardians is released under the MIT License. By contributing to the repository, you agree to release your contributions under the same license.
