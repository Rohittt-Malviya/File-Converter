const MIME_TYPES = {
  txt: "text/plain",
  md: "text/markdown",
  csv: "text/csv",
  json: "application/json",
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  webp: "image/webp"
};

const TEXT_EXTENSIONS = new Set(["txt", "md", "csv", "json"]);
const IMAGE_EXTENSIONS = new Set(["png", "jpg", "jpeg", "webp"]);

export function extensionOf(name) {
  const match = name.toLowerCase().match(/\.([a-z0-9]+)$/);
  return match ? match[1] : "";
}

export function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 ** 2) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1024 ** 2).toFixed(1)} MB`;
}

export function supportedOutputFormats(files) {
  const extensions = new Set(files.map((file) => extensionOf(file.name)));
  if (extensions.size && [...extensions].every((extension) => TEXT_EXTENSIONS.has(extension))) {
    return ["txt", "md", "csv", "json"].filter((format) => !extensions.has(format));
  }
  if (extensions.size && [...extensions].every((extension) => IMAGE_EXTENSIONS.has(extension))) {
    return ["png", "jpg", "webp"].filter((format) => !extensions.has(format));
  }
  return [];
}

function normalizeText(text, sourceExtension, targetExtension) {
  if (targetExtension !== "json" || sourceExtension === "json") return text;
  if (sourceExtension === "csv") {
    const rows = text.trim().split(/\r?\n/).filter(Boolean).map((row) => row.split(",").map((cell) => cell.trim()));
    if (!rows.length) return "[]";
    const [headers, ...values] = rows;
    return JSON.stringify(values.map((row) => Object.fromEntries(headers.map((header, index) => [header, row[index] ?? ""]))), null, 2);
  }
  return JSON.stringify({ content: text }, null, 2);
}

export async function convertText(file, targetExtension) {
  const sourceExtension = extensionOf(file.name);
  const text = await file.text();
  const content = normalizeText(text, sourceExtension, targetExtension);
  return new Blob([content], { type: MIME_TYPES[targetExtension] });
}

export async function convertImage(file, targetExtension) {
  const image = await createImageBitmap(file);
  const canvas = document.createElement("canvas");
  canvas.width = image.width;
  canvas.height = image.height;
  canvas.getContext("2d").drawImage(image, 0, 0);
  image.close();
  return new Promise((resolve, reject) => canvas.toBlob((blob) => blob ? resolve(blob) : reject(new Error("The image could not be converted.")), MIME_TYPES[targetExtension]));
}

export async function convert(file, targetExtension) {
  const sourceExtension = extensionOf(file.name);
  if (TEXT_EXTENSIONS.has(sourceExtension) && TEXT_EXTENSIONS.has(targetExtension)) return convertText(file, targetExtension);
  if (IMAGE_EXTENSIONS.has(sourceExtension) && IMAGE_EXTENSIONS.has(targetExtension)) return convertImage(file, targetExtension);
  throw new Error(`Conversion from ${sourceExtension || "unknown"} to ${targetExtension} is not supported.`);
}

export function outputName(name, targetExtension) {
  return `${name.replace(/\.[^.]+$/, "")}.${targetExtension === "jpg" ? "jpg" : targetExtension}`;
}
