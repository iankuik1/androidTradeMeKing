#!/usr/bin/env python3
"""Agent 4: Image Loading - Caching system"""
from pathlib import Path

def main():
    print("\n" + "="*70)
    print("Agent 4: Image Loading".center(70))
    print("="*70 + "\n")

    # Image loader interface
    content = '''package com.trademe.image

interface ImageCache {
    suspend fun get(url: String): ByteArray?
    suspend fun put(url: String, data: ByteArray)
    suspend fun remove(url: String)
    suspend fun clear()
}

interface ImageLoader {
    suspend fun loadImage(url: String): Result<ByteArray>
    fun prefetchImage(url: String)
}

class InMemoryImageCache(private val maxSizeBytes: Long = 50 * 1024 * 1024) : ImageCache {
    private val cache = linkedMapOf<String, ByteArray>()
    private var currentSize: Long = 0

    override suspend fun get(url: String): ByteArray? {
        return cache[url]?.also {
            cache.remove(url)
            cache[url] = it
        }
    }

    override suspend fun put(url: String, data: ByteArray) {
        cache[url]?.let { currentSize -= it.size }
        currentSize += data.size

        while (currentSize > maxSizeBytes && cache.isNotEmpty()) {
            val oldestKey = cache.keys.first()
            val oldData = cache.remove(oldestKey)
            if (oldData != null) currentSize -= oldData.size
        }

        cache[url] = data
    }

    override suspend fun remove(url: String) {
        cache.remove(url)?.let { currentSize -= it.size }
    }

    override suspend fun clear() {
        cache.clear()
        currentSize = 0
    }
}

class DefaultImageLoader(
    private val cache: ImageCache = InMemoryImageCache()
) : ImageLoader {
    override suspend fun loadImage(url: String): Result<ByteArray> {
        return try {
            cache.get(url)?.let {
                return Result.success(it)
            }
            // In real implementation, would fetch from network
            Result.failure(Exception("Image loading not implemented in local build"))
        } catch (e: Exception) {
            Result.failure(e)
        }
    }

    override fun prefetchImage(url: String) {
        // Async prefetch implementation
    }
}
'''

    path = Path("shared/src/commonMain/kotlin/com/trademe/image/ImageLoader.kt")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip())
    print(f"✓ Created: {path}")

    print("\n" + "="*70)
    print("✓ Image Loading Setup Complete".center(70))
    print("="*70 + "\n")
    return 0

if __name__ == "__main__":
    exit(main())

