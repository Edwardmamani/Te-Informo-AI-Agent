import { Request, Response } from 'express';
import newsScraperService from '../services/news-scraper.service';
import newsAggregatorService from '../services/news-aggregator.service';

/**
 * Controlador para operaciones de noticias
 * Expone herramientas para el agente investigador
 */
export class NewsController {
  /**
   * POST /api/news/search
   * Busca noticias en múltiples fuentes (Google News, BBC, CNN, El País, YouTube)
   * Permite filtrar por intereses del usuario
   */
  async searchNews(req: Request, res: Response): Promise<void> {
    try {
      const { query, userInterests = [] } = req.body;

      // Validación
      if (!query || typeof query !== 'string') {
        res.status(400).json({
          status: 'error',
          message: 'El campo "query" es requerido y debe ser un string'
        });
        return;
      }

      if (!Array.isArray(userInterests)) {
        res.status(400).json({
          status: 'error',
          message: 'El campo "userInterests" debe ser un array'
        });
        return;
      }

      console.log(`📰 Buscando noticias: "${query}" | Intereses: [${userInterests.join(', ')}]`);

      // Buscar noticias usando el servicio de scraping
      const articles = await newsScraperService.searchNews(query, userInterests);

      res.json({
        status: 'success',
        data: {
          articles,
          count: articles.length,
          query,
          userInterests
        }
      });

      console.log(`✅ Noticias encontradas: ${articles.length} artículos`);
    } catch (error: any) {
      console.error('Error en searchNews:', error);
      res.status(500).json({
        status: 'error',
        message: error.message || 'Error al buscar noticias'
      });
    }
  }

  /**
   * POST /api/news/aggregate
   * Obtiene noticias agregadas de múltiples fuentes (método simplificado)
   */
  async aggregateNews(req: Request, res: Response): Promise<void> {
    try {
      const { query } = req.body;

      // Validación
      if (!query || typeof query !== 'string') {
        res.status(400).json({
          status: 'error',
          message: 'El campo "query" es requerido y debe ser un string'
        });
        return;
      }

      console.log(`📰 Agregando noticias: "${query}"`);

      // Obtener noticias usando el servicio agregador
      const articles = await newsAggregatorService.fetchNews(query);

      res.json({
        status: 'success',
        data: {
          articles,
          count: articles.length,
          query
        }
      });

      console.log(`✅ Noticias agregadas: ${articles.length} artículos`);
    } catch (error: any) {
      console.error('Error en aggregateNews:', error);
      res.status(500).json({
        status: 'error',
        message: error.message || 'Error al agregar noticias'
      });
    }
  }

  /**
   * POST /api/news/extract
   * Extrae el contenido completo de un artículo específico
   */
  async extractContent(req: Request, res: Response): Promise<void> {
    try {
      const { url } = req.body;

      // Validación
      if (!url || typeof url !== 'string') {
        res.status(400).json({
          status: 'error',
          message: 'El campo "url" es requerido y debe ser un string'
        });
        return;
      }

      // Validar que sea una URL válida
      try {
        new URL(url);
      } catch {
        res.status(400).json({
          status: 'error',
          message: 'El campo "url" debe ser una URL válida'
        });
        return;
      }

      console.log(`📄 Extrayendo contenido de: ${url}`);

      // Extraer contenido usando el servicio de scraping
      const content = await newsScraperService.extractArticleContent(url);

      res.json({
        status: 'success',
        data: {
          url,
          content,
          contentLength: content.length
        }
      });

      console.log(`✅ Contenido extraído: ${content.length} caracteres`);
    } catch (error: any) {
      console.error('Error en extractContent:', error);
      res.status(500).json({
        status: 'error',
        message: error.message || 'Error al extraer contenido del artículo'
      });
    }
  }

  /**
   * GET /api/news/health
   * Verifica el estado del servicio de noticias
   */
  async health(req: Request, res: Response): Promise<void> {
    try {
      res.json({
        status: 'success',
        message: 'Servicio de noticias operativo',
        services: {
          scraper: 'available',
          aggregator: 'available'
        }
      });
    } catch (error: any) {
      res.status(500).json({
        status: 'error',
        message: error.message || 'Error al verificar el servicio'
      });
    }
  }
}

export default new NewsController();

