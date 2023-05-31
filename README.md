# check_all_english_links

Inputs:

No inputs specified

Secrets:

No secrets specified

Jobs:

| Name | Job ID | Runs On |
| ---- | ------ | ------- |
| Check all links | check_all_english_links | ubuntu-latest |

# test

Inputs:

No inputs specified

Secrets:

No secrets specified

Jobs:

| Name | Job ID | Runs On |
| ---- | ------ | ------- |
| Unnamed job | test | ${{ fromJSON('["ubuntu-latest", "self-hosted"]')[github.repository == 'github/docs-internal'] }} |

# deploy

Inputs:

No inputs specified

Secrets:

No secrets specified

Jobs:

| Name | Job ID | Runs On |
| ---- | ------ | ------- |
| Unnamed job | deploy | ['self-hosted', 'Linux', 'hub'] |

