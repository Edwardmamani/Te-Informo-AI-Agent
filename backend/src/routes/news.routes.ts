import { Router } from 'express';
import newsController from '../controllers/news.controller';

const router = Router();

/**
 * POST /api/news/search
 * Busca noticias en múltiples fuentes (Google News, BBC, CNN, El País, YouTube)
 * Body: { query: string, userInterests?: string[] }
 */
router.post('/search', (req, res) => newsController.searchNews(req, res));

/**
 * POST /api/news/aggregate
 * Obtiene noticias agregadas de múltiples fuentes (método simplificado)
 * Body: { query: string }
 */
router.post('/aggregate', (req, res) => newsController.aggregateNews(req, res));

/**
 * POST /api/news/extract
 * Extrae el contenido completo de un artículo específico
 * Body: { url: string }
 */
router.post('/extract', (req, res) => newsController.extractContent(req, res));

/**
 * GET /api/news/health
 * Verifica el estado del servicio de noticias
 */
router.get('/health', (req, res) => newsController.health(req, res));

export default router;

