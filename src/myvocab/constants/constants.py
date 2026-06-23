# TYPE REPRESENTATION
BOOLEAN_STRINGS = ('true', '1', 'false', '0')
TRUTH_STRINGS  = ('true', '1')
FALSE_STRINGS = ('false', '0')

# IDENTIFIERS
# and their corresponding non-overlapping ranges
UNCHANGED_DATA_ID = -1000
RANGE_SINGULAR_ID = range(1, 1000)
RANGE_SINGULAR_MAX_ID = 1000 - 1
RANGE_INFINIT_ID = range(1000, 2000)
RANGE_INFINIT_MAX_ID = 2000 - 1
RANGE_CASING_ID = range(2000, 3000)
RANGE_CASING_MAX_ID = 3000 - 1

# MARKS
# Tags for controlling text parsing
TAG_WORD = '<<word>>'
TAG_END_WORD = '<</word>>'
TAG_TRANSLATE = '<<tr>>'

# WORD TRANSLATION
# Target chunk size (Yandex Translate API has a 10_000 character limit per request)
TRANSLATE_CHUNK_SIZE = 10_000
# Folder for sent and received translation chunks
TRANSLATE_FOLDER = 'Translate'

# FETCHING YANDEX API
# Endpoint to invoke the public function
URI_FUNC_IAM_TOKENS = 'https://functions.yandexcloud.net/d4ejta7dta3mi7jeti0n'
# Endpoint to exchange a code for a Yandex.OAuth token
URI_IAM_TOKENS = 'https://iam.api.cloud.yandex.net/iam/v1/tokens'
# Endpoint for translation
URI_TRANSLATE = 'https://translate.api.cloud.yandex.net/translate/v2/translate'
# Endpoint for get supported languages
URI_LANGUAGES = 'https://translate.api.cloud.yandex.net/translate/v2/languages'
# Service account folder ID
FOLDER_ID = "b1gq1oofuk6esi44suvt"
