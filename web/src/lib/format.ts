export function percent(value: number) {
  return `${Math.round(value * 1000) / 10}%`;
}

export function compactNumber(value: number) {
  return new Intl.NumberFormat('en', { notation: 'compact' }).format(value);
}
