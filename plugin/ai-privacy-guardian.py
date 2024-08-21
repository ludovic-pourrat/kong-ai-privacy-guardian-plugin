#!/usr/bin/env python3

import kong_pdk.pdk.kong as kong
import spacy
from spacy import Language
from hashlib import sha256

Schema = (
    {"level": {"type": "string", "default": "public", "one_of": ["public", "confidential", "secret"]}},
)

version = '1.0.0'
priority = 0

nlp: Language


def redact(body, entities):
    redacted = ""
    for entity in entities:
        redacted = body[0:entity.start_char] + entity.label_ + "-[" + sha256(
            entity.text.encode('utf-8')).hexdigest() + "]" + body[entity.end_char:]
    return redacted


def sort_entities():
    return lambda item: item.start_char


def process_ner(data, engine):
    document = engine(data)

    entities = []
    # Find named entities, phrases and concepts
    for entity in document.ents:
        label = entity.label_
        if label == 'PERSON':
            entities.append(entity)
        elif label == 'ORG':
            entities.append(entity)
        elif label == 'NOR':
            entities.append(entity)
        elif label == 'NORP':
            entities.append(entity)
        elif label == 'GPE':
            entities.append(entity)
        elif label == 'MISC':
            entities.append(entity)
        else:
            print(entity.label_)

    return sorted(entities, key=sort_entities(), reverse=True)


class Plugin(object):

    def __init__(self, config):
        self.config = config
        global nlp
        nlp = spacy.load("en_core_web_trf")

    def access(self, worker: kong.kong):

        worker.service.request.enable_buffering()
        raw = worker.request.get_raw_body()[0]
        body = raw.decode()

        try:
            if self.config['level'] != "public":
                entities = process_ner(body, nlp)
                for entity in entities:
                    worker.log.info("found entity kind %s" % entity.label_)
                if len(entities) > 0:
                    if self.config['level'] == "confidential":
                        worker.log.warn("sensitive data will be redacted with the confidential classification level")
                        worker.service.request.set_raw_body(redact(body, entities))
                    if self.config['level'] == "secret":
                        worker.log.warn("sensitive data is not allowed with the secret classification level")
                        return worker.response.error(403, "Access Forbidden")
        except Exception as ex:
            worker.log.err("fail to compute data - %s" % ex)

    def response(self, worker: kong.kong):

        worker.log.info("response %s" % kong.service.response.response.get_raw_body())


# add below section to allow this plugin optionally be running in a dedicated process
if __name__ == "__main__":
    from kong_pdk.cli import start_dedicated_server

    start_dedicated_server("ai-privacy-guardian", Plugin, version, priority, Schema)
