import { convert, extensionOf, formatBytes, outputName, supportedOutputFormats } from "./converter.js";

const dropZone = document.querySelector("#drop-zone");
const input = document.querySelector("#file-input");
const queue = document.querySelector("#queue");
const fileList = document.querySelector("#file-list");
const fileCount = document.querySelector("#file-count");
const formatSelect = document.querySelector("#format-select");
const convertButton = document.querySelector("#convert-button");
const clearButton = document.querySelector("#clear-button");
const status = document.querySelector("#status");
let files = [];

function render() {
  queue.hidden = files.length === 0;
  fileCount.textContent = files.length ? `(${files.length})` : "";
  fileList.replaceChildren(...files.map((file) => {
    const row = document.createElement("div");
    row.className = "file-row";
    row.innerHTML = `<span aria-hidden="true">📄</span><strong></strong><span class="file-size"></span>`;
    row.querySelector("strong").textContent = file.name;
    row.querySelector(".file-size").textContent = formatBytes(file.size);
    return row;
  }));
  const formats = supportedOutputFormats(files);
  formatSelect.replaceChildren(...formats.map((format) => new Option(format.toUpperCase(), format)));
  convertButton.disabled = !formats.length;
  if (files.length && !formats.length) status.textContent = "Select files from one compatible format family.";
  else status.textContent = "";
}

function addFiles(selected) {
  files = [...files, ...selected].filter((file, index, list) => list.findIndex((item) => item.name === file.name && item.size === file.size) === index);
  render();
}

async function downloadFile(file, target) {
  const blob = await convert(file, target);
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = outputName(file.name, target);
  link.click();
  setTimeout(() => URL.revokeObjectURL(link.href), 1000);
}

dropZone.addEventListener("click", (event) => {
  if (event.target !== input) input.click();
});
dropZone.addEventListener("keydown", (event) => {
  if (event.key === "Enter" || event.key === " ") input.click();
});
input.addEventListener("change", () => addFiles([...input.files]));
["dragenter", "dragover"].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.add("dragging");
}));
["dragleave", "drop"].forEach((eventName) => dropZone.addEventListener(eventName, (event) => {
  event.preventDefault();
  dropZone.classList.remove("dragging");
}));
dropZone.addEventListener("drop", (event) => addFiles([...event.dataTransfer.files]));
clearButton.addEventListener("click", () => { files = []; input.value = ""; render(); });
convertButton.addEventListener("click", async () => {
  const target = formatSelect.value;
  convertButton.disabled = true;
  status.textContent = "Converting locally…";
  try {
    for (const file of files) await downloadFile(file, target);
    status.textContent = `Converted ${files.length} file${files.length === 1 ? "" : "s"}.`;
  } catch (error) {
    status.textContent = error instanceof Error ? error.message : "Conversion failed.";
  } finally {
    convertButton.disabled = false;
  }
});

render();
