export const REGEX_PATTERNS = {
  PASSWORD:
    /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{6,}$/,
  USERNAME: /^[a-zA-Z0-9_-]{3,20}$/,
} as const;
