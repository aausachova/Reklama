import pako from "pako";

class AnimationCacheService {
  private static instance: AnimationCacheService;
  private cache: Map<string, any> = new Map();

  private constructor() {}

  static getInstance(): AnimationCacheService {
    if (!AnimationCacheService.instance) {
      AnimationCacheService.instance = new AnimationCacheService();
    }
    return AnimationCacheService.instance;
  }

  async getAnimation(src: string): Promise<any> {
    if (this.cache.has(src)) {
      return this.cache.get(src);
    }

    const response = await fetch(src);
    const compressed = await response.arrayBuffer();
    const decompressed = pako.inflate(new Uint8Array(compressed), {
      to: "string",
    });
    const animationData = JSON.parse(decompressed);

    this.cache.set(src, animationData);
    return animationData;
  }
}

export const animationCache = AnimationCacheService.getInstance();
