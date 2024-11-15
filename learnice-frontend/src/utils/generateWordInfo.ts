const wordClassMappings: Record<string, { keys: string[]; mappings: Record<string, string>[] }> = {
    'n': { // Noun
        keys: ['word class', 'gender', 'number', 'case', 'article', 'proper noun'],
        mappings: [
            { 'n': 'noun' },
            { 'k': 'masculine', 'v': 'feminine', 'h': 'neutral' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'nominative', 'o': 'accusative', 'þ': 'dative', 'e': 'genitive' },
            { 'g': 'with suffixed definite article', '-': 'without article' },
            { 's': 'proper noun', '-': 'common noun' }
        ]
    },
    's': { // Verb
        keys: ['word class', 'mood', 'voice', 'person', 'number', 'tense'],
        mappings: [
            { 's': 'verb' },
            { 'n': 'infinitive', 'b': 'imperative', 'f': 'indicative', 'v': 'subjunctive', 'l': 'present participle' },
            { 'g': 'active', 'm': 'middle' },
            { '1': '1st person', '2': '2nd person', '3': '3rd person' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'present', 'þ': 'past'}

        ]
    },
    'l': { // Adjective
        keys: ['word class', 'gender', 'number', 'case', 'declesion', 'degree'],
        mappings: [
            { 'l': 'adjective' },
            { 'k': 'masculine', 'v': 'feminine', 'h': 'neutral' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'nominative', 'o': 'accusative', 'þ': 'dative', 'e': 'genitive' },
            { 's': 'strong declension', 'v': 'weak declension', 'o': 'indeclinable' },
            { 'f': 'positive', 'm': 'comparative', 'e': 'superlative' },
        ]
    },
    'f': { // Pronoun
        keys: ['word class', 'subcategory', 'gender/person', 'number', 'case'],
        mappings: [
            { 'f': 'pronoun' },
            { 'a': 'demonstrative pronoun', 'b': 'indefininte demonstrative pronoun', 'e': 'possessive pronoun', 'o': 'indefinite pronoun', 'p': 'personal pronoun', 's': 'interrogative pronoun', 't': 'relative pronoun' },
            { 'k': 'masculine', 'v': 'feminine', 'h': 'neutral', '1': '1st person', '2': '2nd person' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'nominative', 'o': 'accusative', 'þ': 'dative', 'e': 'genitive' },
        ]
    },
    'g': { // Article
        keys: ['word class', 'gender', 'number', 'case'],
        mappings: [
            { 'g': 'article' },
            { 'k': 'masculine', 'v': 'feminine', 'h': 'neutral' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'nominative', 'o': 'accusative', 'þ': 'dative', 'e': 'genitive' },
        ]
    },
    't': { // Numeral
        keys: ['word class', 'gender', 'number', 'case'],
        mappings: [
            { 't': 'numeral' },
            { 'k': 'masculine', 'v': 'feminine', 'h': 'neutral' },
            { 'e': 'singular', 'f': 'plural' },
            { 'n': 'nominative', 'o': 'accusative', 'þ': 'dative', 'e': 'genitive' },
        ]
    },
    'a': { // Adverb
        keys: ['word class', 'governor', 'degree'],
        mappings: [
            { 'a': 'adverb' },
            { 'a': 'does not govern case', 'f': 'governs case', 'u': 'exclamation' },
            { 'm': 'comparative', 'e': 'superlative' },
        ]
    },
    'c': { // Conjunction
        keys: ['word class', 'category'],
        mappings: [
            { 'c': 'conjunction' },
            { 'n': 'sign of infinitive', 't': 'relative conjunction' },
        ]
    },
    'k': { // Abbreviation
        keys: ['word class', 'category'],
        mappings: [
            { 'k': 'abbreviation' },
            { 's': 'abbreviation', 't': 'short form' },
        ]
    },
    'e': { // Abbreviation
        keys: ['word class'],
        mappings: [
            { 'e': 'foreign word' },
        ]
    },
    'x': { // Abbreviation
        keys: ['word class'],
        mappings: [
            { 'x': 'unknown word' },
        ]
    },
    'v': { // Abbreviation
        keys: ['word class'],
        mappings: [
            { 'v': 'email/web address' },
        ]
    },
    'p': { // Abbreviation
        keys: ['word class', 'category'],
        mappings: [
            { 'p': 'punctuation mark' },
            { 'l': 'end of sentence', 'k': 'comma', 'g': 'quotes', 'a': 'others'}
        ]
    },
    'm': { // Abbreviation
        keys: ['word class'],
        mappings: [
            { 'm': 'symbol' },
        ]
    },
};

// Function to parse PoS tag dynamically based on word class
export function parseDynamicPosTag(tag: string): Record<string, string> {
    const wordClassChar = tag[0]; // First character determines word class
    const mapping = wordClassMappings[wordClassChar];

    if (!mapping) {
        throw new Error(`Unknown word class: ${wordClassChar}`);
    }

    const { keys, mappings } = mapping;
    const attributes: Record<string, string> = {};

    for (let i = 0; i < tag.length; i++) {
        const char = tag[i];
        if (mappings[i] && mappings[i][char]) {
            attributes[keys[i]] = mappings[i][char];
        }
    }

    return attributes;
}