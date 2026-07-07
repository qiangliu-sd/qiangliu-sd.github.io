// worker.js — runs option.wasm off the main thread (plan step 4), so a
// 100,000-path Monte Carlo never freezes the form. Lives in wasm\ next to
// option.js; loaded as a module worker by ..\index.html, which receives
// the engine's log lines relayed via postMessage.

import createModule from './option.js';

// Emscripten's std::random_device (used when fixed_rand_seed=false) fills a
// heap view via crypto.getRandomValues, which — like TextDecoder — rejects
// views backed by the resizable ArrayBuffer that -sALLOW_MEMORY_GROWTH
// produces. Fall back to filling a copy and writing it back.
{
  const orig = crypto.getRandomValues.bind(crypto);
  crypto.getRandomValues = view => {
    try { return orig(view); }
    catch {
      const tmp = new Uint8Array(view.byteLength);
      orig(tmp);
      new Uint8Array(view.buffer, view.byteOffset, view.byteLength).set(tmp);
      return view;
    }
  };
}

const N_OUT = 8;                       // doubles reserved for px_out

const mod = await createModule({
  onLog: (channel, text) => postMessage({ type: 'log', channel, text })
});
postMessage({ type: 'ready', build: mod._ql_wasm_build_date() });

self.onmessage = ({ data: { seq, isPx, payload } }) => {
  const nBytes = mod.lengthBytesUTF8(payload) + 1;
  const pStr = mod._malloc(nBytes);
  mod.stringToUTF8(payload, pStr, nBytes);
  const pOut = mod._malloc(N_OUT * 8);
  mod.HEAPF64.fill(0, pOut >> 3, (pOut >> 3) + N_OUT);
  const t0 = performance.now();
  try {
    const rc = mod._pxDeltaGamma_impVol(isPx ? 1 : 0, pStr, pOut);
    // re-read HEAPF64 after the call: memory growth invalidates old views
    const out = Array.from(mod.HEAPF64.subarray(pOut >> 3, (pOut >> 3) + N_OUT));
    postMessage({ type: 'result', seq, rc, out, ms: performance.now() - t0 });
  } catch (e) {
    postMessage({ type: 'result', seq, rc: 'threw', error: String(e),
                  out: [], ms: performance.now() - t0 });
  } finally {
    mod._free(pStr);
    mod._free(pOut);
  }
};
