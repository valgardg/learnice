export type Noun = {
    wordclass: string;
    gender: string;
    number: string;
    case: string;
    article: string;
    proper_noun: string;
}

export type Adjective = {
    wordclass: string;
    gender: string;
    number: string;
    case: string;
    declesion: string;
    degree: string;
}

export type Pronoun = {
    wordclass: string;
    subcategory: string;
    gender_person: string;
    number: string;
    case: string;
}

export type Article = {
    wordclass: string;
    gender: string;
    number: string;
    case: string;
}

export type Numeral = {
    wordclass: string;
    gender: string;
    number: string;
    case: string;
}

export type Verb = {
    wordclass: string;
    mood: string;
    voice: string;
    gender: string;
    number: string;
    case: string;
}

export type Adverb = {
    wordclass: string;
    category_case: string;
    governor: string;
    degree: string;
}

export type Conjunction = {
    wordclass: string;
    category: string;
}

export type Abbreviation = {
    wordclass: string;
    category: string;
}

export type ForeignWord = {
    wordclass: string;
}

export type UnanalysedWord = {
    wordclass: string;
}

export type EmailWebAddress = {
    wordclass: string;
}

export type Punctuation = {
    wordclass: string;
    category: string;
}

export type Symbol = {
    wordclass: string;
}