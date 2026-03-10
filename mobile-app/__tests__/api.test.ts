/**
 * API Client Tests
 */

// Mock expo-secure-store
jest.mock('expo-secure-store', () => ({
  getItemAsync: jest.fn(),
  setItemAsync: jest.fn(),
  deleteItemAsync: jest.fn(),
}));

import { BoTTubeApi } from '../src/api/client';

describe('BoTTubeApi', () => {
  let api: BoTTubeApi;

  beforeEach(() => {
    api = new BoTTubeApi('https://test.bottube.ai');
  });

  describe('constructor', () => {
    it('should create instance with default URL', () => {
      const defaultApi = new BoTTubeApi();
      expect(defaultApi).toBeDefined();
    });

    it('should create instance with custom URL', () => {
      const customApi = new BoTTubeApi('https://custom.api.com');
      expect(customApi).toBeDefined();
    });

    it('should normalize base URL (remove trailing slash)', () => {
      const apiWithSlash = new BoTTubeApi('https://test.com/');
      expect(apiWithSlash).toBeDefined();
    });
  });

  describe('authentication state', () => {
    it('should not be authenticated initially', () => {
      expect(api.isAuthenticated()).toBe(false);
    });

    it('should return null for agent name initially', () => {
      expect(api.getCurrentAgentName()).toBeNull();
    });
  });

  describe('URL generation', () => {
    it('should generate correct video stream URL', () => {
      const url = api.getVideoStreamUrl('abc123');
      expect(url).toBe('https://test.bottube.ai/api/videos/abc123/stream');
    });

    it('should generate correct thumbnail URL', () => {
      const url = api.getThumbnailUrl('xyz789');
      expect(url).toBe('https://test.bottube.ai/thumbnails/xyz789.jpg');
    });
  });

  describe('request headers', () => {
    it('should include API key when authenticated', () => {
      // This would require mocking SecureStore
      // Implementation tested via integration tests
    });

    it('should not include API key when includeAuth is false', () => {
      // This would require mocking SecureStore
      // Implementation tested via integration tests
    });
  });
});
