#!/usr/bin/env bun

import { BunRuntime } from "@effect/platform-bun"
import { Layer } from "effect"
import { ServerLayer } from "./Mcp.js"

Layer.launch(ServerLayer).pipe(BunRuntime.runMain)
