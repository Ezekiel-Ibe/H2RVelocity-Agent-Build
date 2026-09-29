import "@testing-library/jest-dom";
import * as axeMatchers from "vitest-axe/matchers";
import { expect, beforeAll, afterEach, afterAll } from "vitest";
import { server } from "@/mocks/server";

expect.extend(axeMatchers);

beforeAll(() => server.listen({ onUnhandledRequest: "bypass" }));
afterEach(() => server.resetHandlers());
afterAll(() => server.close());
