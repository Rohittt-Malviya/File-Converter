import test from "node:test";
import assert from "node:assert/strict";
import { extensionOf, formatBytes, outputName, supportedOutputFormats } from "../src/converter.js";

test("reads file extensions safely", () => {
  assert.equal(extensionOf("report.JSON"), "json");
  assert.equal(extensionOf("README"), "");
});

test("formats byte sizes", () => {
  assert.equal(formatBytes(512), "512 B");
  assert.equal(formatBytes(2048), "2.0 KB");
});

test("returns compatible output formats", () => {
  assert.deepEqual(supportedOutputFormats([{ name: "a.txt" }, { name: "b.md" }]), ["csv", "json"]);
  assert.deepEqual(supportedOutputFormats([{ name: "a.png" }]), ["jpg", "webp"]);
  assert.deepEqual(supportedOutputFormats([{ name: "a.txt" }, { name: "b.png" }]), []);
});

test("creates output names", () => {
  assert.equal(outputName("photo.PNG", "jpg"), "photo.jpg");
});
