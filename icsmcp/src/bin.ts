#!/usr/bin/env bun

import { BunRuntime } from "@effect/platform-bun";
import { ServerLayer } from "./Mcp.js";
import { Layer } from "effect";

Layer.launch(ServerLayer).pipe(BunRuntime.runMain);
