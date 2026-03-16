import { describe, it, expect, vi, beforeEach } from 'vitest';
import { actorApi } from './lib/api';

describe('Registration Flow API', () => {
  beforeEach(() => {
    vi.stubGlobal('fetch', vi.fn());
  });

  it('should call register API and return response on success', async () => {
    const mockResponse = { id: 'uuid', username: 'testuser' };
    (fetch as any).mockResolvedValue({
      status: 201,
      ok: true,
      json: async () => mockResponse
    });

    const result = await actorApi.register('testuser', 'password123');

    expect(fetch).toHaveBeenCalledWith('/api/auth/register', expect.objectContaining({
      method: 'POST',
      body: JSON.stringify({ username: 'testuser', password: 'password123' })
    }));
    expect(result).toEqual(mockResponse);
  });

  it('should throw error on registration failure', async () => {
    (fetch as any).mockResolvedValue({
      status: 400,
      ok: false,
      json: async () => ({ error: 'User already exists' })
    });

    await expect(actorApi.register('existing', 'pass')).rejects.toThrow('User already exists');
  });

  it('should throw generic error if response is not ok and no error message', async () => {
    (fetch as any).mockResolvedValue({
      status: 500,
      ok: false,
      json: async () => ({})
    });

    await expect(actorApi.register('fail', 'pass')).rejects.toThrow('Request failed');
  });
});
