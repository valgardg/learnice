export function isPunctuation(char: string) {
    const punctuationRegex = /[!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~]/;
    return punctuationRegex.test(char);
  }