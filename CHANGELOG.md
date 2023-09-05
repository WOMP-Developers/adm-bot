# Changelog

<!--next-version-placeholder-->

## v2.2.0 (2023-09-05)
### Feature
* Improve database connection error management ([`b292faa`](https://github.com/agelito/adm-bot/commit/b292faaae35e4baba77465aa5b6aab8ec40cb988))

## v2.1.4 (2023-08-18)
### Fix
* Round adm sum ([`c100a27`](https://github.com/agelito/adm-bot/commit/c100a2771f15580dfd1cbae3e79c49aff448d2a9))

### Documentation
* Add email address to authors field ([`7ebe781`](https://github.com/agelito/adm-bot/commit/7ebe781ea88ee41ecbe532754fe9f80e8440d8e0))

## v2.1.3 (2023-08-15)
### Fix
* Rollback mysql on OperationalError ([`497fd26`](https://github.com/agelito/adm-bot/commit/497fd2675c57ddc3d5e7d5b904b082c8083348c9))
* Set connnection pool size to 5 ([`1e85870`](https://github.com/agelito/adm-bot/commit/1e8587047a5e3a6a1fc3ba85b3615f1a02551e69))

## v2.1.2 (2023-08-13)
### Fix
* Interrupt the application on SIGTERM signal ([`0c67818`](https://github.com/agelito/adm-bot/commit/0c678181c6a3b9cd6194b3e460de32b420f752f1))
* Respond to commands even if there's no data ([`abe2ca1`](https://github.com/agelito/adm-bot/commit/abe2ca1fa6535f9eebda0d0657b49473b33c05e9))

## v2.1.1 (2023-08-11)
### Fix
* Issue reading guild_id during commands sync ([`e9f035e`](https://github.com/agelito/adm-bot/commit/e9f035eb855b660150f59adda83c233291ca0904))

## v2.1.0 (2023-08-08)
### Feature
* Add option to ignore TCU when collecting adm ([`2c0a414`](https://github.com/agelito/adm-bot/commit/2c0a4142797bc09501acefc5fd9b186c2b4051e0))

### Fix
* Query compatibility with sqlite ([`53b20c9`](https://github.com/agelito/adm-bot/commit/53b20c99ad58cdc3b595ab15f041a9feb7fd0738))

## v2.0.0 (2023-08-07)
### Feature
* Add support for mysql database ([#25](https://github.com/agelito/adm-bot/issues/25)) ([`8e42139`](https://github.com/agelito/adm-bot/commit/8e42139e431b1264f8494cb55cd171ebb4767c69))

### Breaking
* add support for mysql database ([#25](https://github.com/agelito/adm-bot/issues/25)) ([`8e42139`](https://github.com/agelito/adm-bot/commit/8e42139e431b1264f8494cb55cd171ebb4767c69))

## v1.3.2 (2023-07-03)
### Fix
* History graph ylim set to 6.2 ([`9ffa9f1`](https://github.com/agelito/adm-bot/commit/9ffa9f1c53dae330b4ff4a3f81551dbccd9d8632))

## v1.3.1 (2023-05-24)


## v1.3.0 (2023-05-21)
### Feature
* Add separate command to synchronize slash commands ([`7016c13`](https://github.com/agelito/adm-bot/commit/7016c136470aaad7121010284e36f2b09fa8c5f2))

## v1.2.5 (2023-05-21)
### Fix
* Set bot command_prefix ([`6cd8bac`](https://github.com/agelito/adm-bot/commit/6cd8bac3e9accf055ea211e68608cc073733cd03))

## v1.2.4 (2023-05-20)


## v1.2.3 (2023-05-20)
### Fix
* Support python38 ([#14](https://github.com/agelito/adm-bot/issues/14)) ([`cd40d83`](https://github.com/agelito/adm-bot/commit/cd40d8361d2c44b2b20c58a4c9c16bfc7add392d))

## v1.2.2 (2023-05-19)
### Fix
* Remove duplicte command in startup message ([#13](https://github.com/agelito/adm-bot/issues/13)) ([`52f5a02`](https://github.com/agelito/adm-bot/commit/52f5a02e1a94fdc063068f9586a122af2379f0c2))

## v1.2.1 (2023-05-18)
### Fix
* Improved bot startup message ([#12](https://github.com/agelito/adm-bot/issues/12)) ([`f8c06bb`](https://github.com/agelito/adm-bot/commit/f8c06bb1a61d73de01a66694d910623efae50c80))

## v1.2.0 (2023-05-18)
### Feature
* Automatically purge adm data after days ([#11](https://github.com/agelito/adm-bot/issues/11)) ([`d333bfa`](https://github.com/agelito/adm-bot/commit/d333bfa1efae549a1a84362e8b3f21e930b258ac))

## v1.1.2 (2023-05-18)
### Documentation
* Correct readme for update command ([#10](https://github.com/agelito/adm-bot/issues/10)) ([`ed615a9`](https://github.com/agelito/adm-bot/commit/ed615a9fee91f546f9641fcb21ad113b7d7bfc3f))

## v1.1.1 (2023-05-17)
### Documentation
* Update badge links ([#9](https://github.com/agelito/adm-bot/issues/9)) ([`f404fb0`](https://github.com/agelito/adm-bot/commit/f404fb0c5bc8783a3a9da6bb89530d338ad97ba9))

## v1.1.0 (2023-05-17)
### Feature
* Modal view to manually update system adm ([#8](https://github.com/agelito/adm-bot/issues/8)) ([`e36835b`](https://github.com/agelito/adm-bot/commit/e36835b4143aa5da35d76281b3695e9095633292))

## v1.0.7 (2023-05-17)


## v1.0.6 (2023-05-17)


## v1.0.5 (2023-05-16)
### Documentation
* Add some nice badges ([`588e548`](https://github.com/agelito/adm-bot/commit/588e54875f40794097fd684dcf20d0db5713e54c))

## v1.0.4 (2023-05-16)
### Documentation
* Improved quick start guide ([`2bd7ca7`](https://github.com/agelito/adm-bot/commit/2bd7ca7926b1e06055090f3fea5e26be49a21070))

## v1.0.3 (2023-05-16)
### Documentation
* Add repository field ([`28a8ab8`](https://github.com/agelito/adm-bot/commit/28a8ab8537b0fc4cc75166398c4192b8e80363e8))

## v1.0.2 (2023-05-16)
### Documentation
* Update quick start section for pip ([`0a25a39`](https://github.com/agelito/adm-bot/commit/0a25a39f67ebc294b384e3cdcee7cc30005e3edf))

## v1.0.1 (2023-05-16)
### Fix
* Set auto refresh interrupt after bot run ([`8b18dfe`](https://github.com/agelito/adm-bot/commit/8b18dfe7c458386605040751c149b64dffca4a70))
