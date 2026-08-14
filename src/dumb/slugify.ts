// Mirrors cms/phrases/audio.py's audio_filename slug (lowercase, non-alnum
// runs collapsed to a single hyphen) so audio URLs can be derived from the
// phrase text without a lookup table.
export function slugify(text: string): string {
  return text.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '')
}
