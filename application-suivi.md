# 🎯 Application de Suivi des Candidatures

## 📋 Vue d'Ensemble

Application web complète pour le suivi et la gestion des candidatures d'emploi basée sur les données LinkedIn scrappées. Interface moderne avec Next.js, base de données PostgreSQL et composants Shadcn/Radix pour une expérience utilisateur optimale.

## 🏗️ Architecture Technique

```
Next.js Frontend (Shadcn/Radix) ↔ Prisma ORM ↔ PostgreSQL Database
```

### Stack Technologique

- **Frontend** : Next.js 14 + TypeScript + Tailwind CSS
- **UI Components** : Shadcn/ui + Radix UI
- **Backend** : Next.js API Routes + Prisma ORM
- **Base de données** : PostgreSQL
- **Authentification** : NextAuth.js (optionnel)
- **Styling** : Tailwind CSS + CSS Variables

## 🗄️ Schéma de Base de Données

```prisma
// schema.prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Job {
  id                  String   @id // ID LinkedIn original
  title              String
  company            String
  companyUrl         String?
  location           String
  description        String   @db.Text
  linkedinUrl        String
  applyUrl           String?
  listedAt           DateTime
  workplaceType      String?  // Remote, Hybrid, On-site
  jobNature          String?  // Full-time, Part-time, etc.
  workRemoteAllowed  Boolean  @default(false)
  customLogoUrl      String?
  
  // Nouveaux champs de suivi
  applicationStatus  ApplicationStatus @default(NOT_VIEWED)
  priority          Priority          @default(MEDIUM)
  isBookmarked      Boolean           @default(false)
  applicationDate   DateTime?
  responseDate      DateTime?
  interviewDate     DateTime?
  salaryMin         Int?
  salaryMax         Int?
  
  // Relations
  notes             Note[]
  contacts          Contact[]
  tags              JobTag[]
  
  createdAt         DateTime @default(now())
  updatedAt         DateTime @updatedAt
  
  @@map("jobs")
}

model Note {
  id        String   @id @default(cuid())
  content   String   @db.Text
  type      NoteType @default(GENERAL)
  jobId     String
  job       Job      @relation(fields: [jobId], references: [id], onDelete: Cascade)
  createdAt DateTime @default(now())
  
  @@map("notes")
}

model Contact {
  id          String  @id @default(cuid())
  name        String
  role        String?
  email       String?
  phone       String?
  linkedin    String?
  notes       String?
  jobId       String
  job         Job     @relation(fields: [jobId], references: [id], onDelete: Cascade)
  createdAt   DateTime @default(now())
  
  @@map("contacts")
}

model Tag {
  id    String   @id @default(cuid())
  name  String   @unique
  color String   @default("#3B82F6")
  jobs  JobTag[]
  
  @@map("tags")
}

model JobTag {
  jobId String
  tagId String
  job   Job    @relation(fields: [jobId], references: [id], onDelete: Cascade)
  tag   Tag    @relation(fields: [tagId], references: [id], onDelete: Cascade)
  
  @@id([jobId, tagId])
  @@map("job_tags")
}

enum ApplicationStatus {
  NOT_VIEWED
  REVIEWED
  INTERESTED
  NOT_INTERESTED
  APPLIED
  PHONE_SCREEN
  INTERVIEW_SCHEDULED
  INTERVIEW_COMPLETED
  REJECTED
  OFFER_RECEIVED
  ACCEPTED
  DECLINED
}

enum Priority {
  LOW
  MEDIUM
  HIGH
  URGENT
}

enum NoteType {
  GENERAL
  INTERVIEW
  RESEARCH
  CONTACT
  FOLLOW_UP
}
```

## 📱 Interfaces Utilisateur

### 1. Dashboard Principal
- **Vue kanban** par statut d'application
- **Statistiques** de candidatures (total, en cours, rejetées, acceptées)
- **Offres récentes** et prioritaires
- **Graphiques de progression** temporelle
- **Métriques de performance** (taux de réponse, temps de processus)

### 2. Liste des Offres
- **Tableau complet** avec tri/filtrage avancé
- **Recherche full-text** dans titre, entreprise, description
- **Filtres multiples** par statut, priorité, tags, localisation
- **Actions rapides** (bookmark, statut, notes)
- **Vue grille** ou tableau selon préférence
- **Export** des résultats filtrés

### 3. Détail d'une Offre
- **Informations complètes** de l'offre LinkedIn
- **Gestion du statut** avec timeline visuelle
- **Système de priorité** avec indicateurs visuels
- **Ajout de notes** avec éditeur rich text
- **Gestion des contacts** liés à l'offre
- **Tags personnalisés** avec couleurs
- **Timeline des actions** et modifications

### 4. Gestion des Contacts
- **Liste des contacts** par offre d'emploi
- **Informations complètes** (nom, rôle, email, téléphone, LinkedIn)
- **Historique des interactions** et communications
- **Notes de suivi** par contact
- **Rappels automatiques** pour le suivi

### 5. Analytics et Reporting
- **Tableaux de bord** interactifs
- **Métriques détaillées** par période
- **Analyse par entreprise** et secteur
- **Taux de conversion** par étape
- **Export des données** en différents formats

## 📁 Structure du Projet

```
job-tracker/
├── prisma/
│   ├── schema.prisma
│   ├── migrations/
│   └── seed.ts              # Migration des données JSON
├── src/
│   ├── app/
│   │   ├── (dashboard)/
│   │   │   ├── page.tsx     # Dashboard principal
│   │   │   ├── jobs/
│   │   │   │   ├── page.tsx # Liste des offres
│   │   │   │   └── [id]/
│   │   │   │       └── page.tsx # Détail offre
│   │   │   ├── contacts/
│   │   │   │   └── page.tsx # Gestion contacts
│   │   │   ├── analytics/
│   │   │   │   └── page.tsx # Analytics
│   │   │   └── settings/
│   │   │       └── page.tsx # Paramètres
│   │   ├── api/
│   │   │   ├── jobs/
│   │   │   │   ├── route.ts
│   │   │   │   └── [id]/
│   │   │   │       └── route.ts
│   │   │   ├── notes/
│   │   │   │   └── route.ts
│   │   │   ├── contacts/
│   │   │   │   └── route.ts
│   │   │   ├── tags/
│   │   │   │   └── route.ts
│   │   │   └── import/
│   │   │       └── route.ts # Import JSON existant
│   │   ├── globals.css
│   │   ├── layout.tsx
│   │   └── loading.tsx
│   ├── components/
│   │   ├── ui/              # Shadcn components
│   │   │   ├── button.tsx
│   │   │   ├── input.tsx
│   │   │   ├── select.tsx
│   │   │   ├── dialog.tsx
│   │   │   ├── table.tsx
│   │   │   ├── badge.tsx
│   │   │   └── ...
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   └── Footer.tsx
│   │   ├── jobs/
│   │   │   ├── JobCard.tsx
│   │   │   ├── JobTable.tsx
│   │   │   ├── JobKanban.tsx
│   │   │   ├── JobDetail.tsx
│   │   │   ├── JobFilters.tsx
│   │   │   └── JobStatusBadge.tsx
│   │   ├── notes/
│   │   │   ├── NoteEditor.tsx
│   │   │   ├── NoteList.tsx
│   │   │   └── NoteCard.tsx
│   │   ├── contacts/
│   │   │   ├── ContactForm.tsx
│   │   │   ├── ContactList.tsx
│   │   │   └── ContactCard.tsx
│   │   ├── analytics/
│   │   │   ├── StatsCard.tsx
│   │   │   ├── ChartComponent.tsx
│   │   │   └── MetricsGrid.tsx
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       ├── ErrorBoundary.tsx
│   │       └── Pagination.tsx
│   ├── lib/
│   │   ├── prisma.ts
│   │   ├── utils.ts
│   │   ├── validations.ts
│   │   ├── constants.ts
│   │   └── api-client.ts
│   ├── hooks/
│   │   ├── useJobs.ts
│   │   ├── useNotes.ts
│   │   ├── useContacts.ts
│   │   └── useAnalytics.ts
│   └── types/
│       ├── index.ts
│       ├── job.ts
│       ├── note.ts
│       └── contact.ts
├── public/
│   ├── icons/
│   └── images/
├── package.json
├── next.config.js
├── tailwind.config.js
├── components.json         # Shadcn config
├── .env.local
├── .env.example
└── README.md
```

## 🚀 Fonctionnalités Principales

### 1. Gestion des Statuts d'Application
- **Pipeline complet** : Non vue → Examinée → Intéressé → Candidature envoyée → Entretien → Offre → Acceptée/Refusée
- **Transitions automatiques** avec dates de mise à jour
- **Notifications** de suivi automatiques
- **Rappels** pour actions en attente

### 2. Système de Notes Avancé
- **Notes par type** : Général, Entretien, Recherche, Contact, Suivi
- **Éditeur rich text** avec formatage
- **Timestamps** automatiques
- **Recherche** dans les notes
- **Attachements** de fichiers (CV adapté, lettres de motivation)

### 3. Gestion Complète des Contacts
- **Informations détaillées** par contact
- **Historique des interactions** avec dates
- **Notes de suivi** spécifiques
- **Intégration LinkedIn** automatique
- **Rappels de relance** programmés

### 4. Système de Tags et Organisation
- **Tags colorés** personnalisés
- **Catégorisation flexible** (secteur, type d'entreprise, source, etc.)
- **Filtrage avancé** par combinaisons de tags
- **Organisation visuelle** intuitive

### 5. Analytics et Métriques
- **Tableaux de bord** en temps réel
- **Métriques de performance** (taux de réponse, temps de processus)
- **Analyse par période** (semaine, mois, trimestre)
- **Comparaisons** entre entreprises et secteurs
- **Graphiques interactifs** pour visualisation

### 6. Import et Synchronisation
- **Import automatique** des données JSON existantes
- **Synchronisation** avec nouvelles recherches
- **Détection de doublons** intelligente
- **Mise à jour** des informations existantes

## 🔄 Migration des Données

### Script de Migration Automatique

```typescript
// prisma/seed.ts
import { PrismaClient } from '@prisma/client';
import fs from 'fs';
import path from 'path';

const prisma = new PrismaClient();

async function migrateJobsFromJSON() {
  console.log('🚀 Démarrage de la migration des données JSON...');
  
  const jsonPath = path.join(__dirname, '../../Exports/linkedin_job_searches_consolidated.json');
  const jsonData = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
  
  let migratedCount = 0;
  let skippedCount = 0;
  
  for (const job of jsonData.jobs) {
    try {
      const existingJob = await prisma.job.findUnique({
        where: { id: job.id }
      });
      
      if (existingJob) {
        skippedCount++;
        continue;
      }
      
      await prisma.job.create({
        data: {
          id: job.id,
          title: job.title,
          company: job.company,
          companyUrl: job.company_url,
          location: job.location,
          description: job.description,
          linkedinUrl: job.linkedin_postJob_url,
          applyUrl: job.apply_url,
          listedAt: new Date(job.listed_at),
          workplaceType: job.workplace_type,
          jobNature: job.job_nature,
          workRemoteAllowed: job.work_remote_allowed,
          customLogoUrl: job.custom_logo_url,
          // Valeurs par défaut pour les nouveaux champs
          applicationStatus: 'NOT_VIEWED',
          priority: 'MEDIUM',
          isBookmarked: false
        }
      });
      
      migratedCount++;
    } catch (error) {
      console.error(`Erreur lors de la migration de l'offre ${job.id}:`, error);
    }
  }
  
  console.log(`✅ Migration terminée:`);
  console.log(`   - ${migratedCount} offres migrées`);
  console.log(`   - ${skippedCount} offres déjà existantes`);
}

async function createDefaultTags() {
  const defaultTags = [
    { name: 'Priorité haute', color: '#EF4444' },
    { name: 'Remote possible', color: '#10B981' },
    { name: 'Startup', color: '#8B5CF6' },
    { name: 'Grande entreprise', color: '#3B82F6' },
    { name: 'Tech', color: '#06B6D4' },
    { name: 'Marketing', color: '#F59E0B' },
    { name: 'SEO', color: '#84CC16' }
  ];
  
  for (const tag of defaultTags) {
    await prisma.tag.upsert({
      where: { name: tag.name },
      update: {},
      create: tag
    });
  }
  
  console.log('✅ Tags par défaut créés');
}

async function main() {
  await migrateJobsFromJSON();
  await createDefaultTags();
  
  console.log('🎉 Migration complète terminée !');
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await prisma.$disconnect();
  });
```

## 🎯 Phases de Développement

### Phase 1 : Setup et Migration (Semaine 1)
- ✅ Configuration Next.js + TypeScript + Tailwind
- ✅ Setup PostgreSQL et Prisma
- ✅ Migration des 492 offres existantes
- ✅ Interface de base avec Shadcn
- ✅ Authentification (optionnelle)

### Phase 2 : Core Features (Semaine 2)
- ✅ CRUD complet pour les offres
- ✅ Système de statuts d'application
- ✅ Interface liste et détail des offres
- ✅ Système de priorités
- ✅ Bookmarks et favoris

### Phase 3 : Features Avancées (Semaine 3)
- ✅ Système de notes avec types
- ✅ Gestion des contacts
- ✅ Tags personnalisés
- ✅ Filtres et recherche avancée
- ✅ Vue kanban par statut

### Phase 4 : Analytics et Polish (Semaine 4)
- ✅ Dashboard analytics complet
- ✅ Métriques et graphiques
- ✅ Export des données
- ✅ Optimisations performance
- ✅ Tests et débogage

## 💻 Installation et Configuration

### Prérequis
- Node.js 18+ 
- PostgreSQL 14+
- npm ou yarn

### Commandes de Démarrage

```bash
# 1. Créer le projet Next.js
npx create-next-app@latest job-tracker --typescript --tailwind --app --src-dir
cd job-tracker

# 2. Installation des dépendances principales
npm install prisma @prisma/client
npm install @radix-ui/react-dialog @radix-ui/react-select @radix-ui/react-tabs
npm install @radix-ui/react-dropdown-menu @radix-ui/react-alert-dialog
npm install lucide-react class-variance-authority clsx tailwind-merge
npm install react-hook-form @hookform/resolvers zod
npm install recharts date-fns

# 3. Installation des dépendances de développement
npm install -D @types/node tsx

# 4. Initialiser Shadcn UI
npx shadcn-ui@latest init
npx shadcn-ui@latest add button input select dialog table badge
npx shadcn-ui@latest add card tabs dropdown-menu alert-dialog
npx shadcn-ui@latest add form textarea checkbox switch

# 5. Initialiser Prisma
npx prisma init

# 6. Configuration de la base de données
# Éditer .env.local avec les informations PostgreSQL
echo "DATABASE_URL='postgresql://username:password@localhost:5432/job_tracker'" >> .env.local

# 7. Générer et exécuter les migrations
npx prisma migrate dev --name init

# 8. Seed de la base de données
npx prisma db seed

# 9. Générer le client Prisma
npx prisma generate

# 10. Lancer l'application
npm run dev
```

### Configuration PostgreSQL

```sql
-- Création de la base de données
CREATE DATABASE job_tracker;
CREATE USER job_tracker_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE job_tracker TO job_tracker_user;
```

### Variables d'Environnement

```bash
# .env.local
DATABASE_URL="postgresql://job_tracker_user:secure_password@localhost:5432/job_tracker"
NEXTAUTH_SECRET="your-secret-key-here"
NEXTAUTH_URL="http://localhost:3000"
```

## 🔧 Configuration Technique

### package.json
```json
{
  "name": "job-tracker",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start",
    "lint": "next lint",
    "db:migrate": "prisma migrate dev",
    "db:seed": "tsx prisma/seed.ts",
    "db:studio": "prisma studio"
  },
  "dependencies": {
    "next": "14.0.0",
    "react": "18.0.0",
    "react-dom": "18.0.0",
    "@prisma/client": "^5.0.0",
    "prisma": "^5.0.0",
    "@radix-ui/react-dialog": "^1.0.5",
    "@radix-ui/react-select": "^2.0.0",
    "lucide-react": "^0.290.0",
    "tailwindcss": "^3.3.0",
    "typescript": "^5.0.0"
  }
}
```

### next.config.js
```javascript
/** @type {import('next').NextConfig} */
const nextConfig = {
  experimental: {
    serverComponentsExternalPackages: ['@prisma/client']
  },
  images: {
    domains: ['media.licdn.com', 'media-exp1.licdn.com']
  }
};

module.exports = nextConfig;
```

## 🎨 Design System

### Couleurs et Thème
- **Primary** : Blue (#3B82F6)
- **Success** : Green (#10B981) 
- **Warning** : Orange (#F59E0B)
- **Error** : Red (#EF4444)
- **Neutral** : Gray (#6B7280)

### Composants UI Standards
- **Buttons** : Shadcn button variants
- **Forms** : React Hook Form + Zod validation
- **Tables** : Shadcn table avec tri et pagination
- **Dialogs** : Radix UI modals
- **Charts** : Recharts pour analytics

## 📊 Métriques et Performance

### Objectifs de Performance
- **Temps de chargement** : < 2 secondes
- **First Contentful Paint** : < 1.5 secondes
- **Largest Contentful Paint** : < 2.5 secondes
- **Cumulative Layout Shift** : < 0.1

### Optimisations Prévues
- **SSR/SSG** pour les pages statiques
- **Image optimization** avec Next.js Image
- **Database indexing** sur les champs fréquemment utilisés
- **Pagination** pour les grandes listes
- **Lazy loading** des composants lourds

## 🔒 Sécurité

### Mesures de Sécurité
- **Validation** côté client et serveur avec Zod
- **Sanitization** des inputs utilisateur
- **CSRF protection** intégrée Next.js
- **SQL injection** prévention via Prisma ORM
- **Rate limiting** sur les API routes

## 🚀 Déploiement

### Options de Déploiement
- **Vercel** (recommandé pour Next.js)
- **Railway** (pour PostgreSQL inclus)
- **DigitalOcean App Platform**
- **AWS/GCP/Azure** avec containers Docker

### Checklist de Production
- [ ] Variables d'environnement configurées
- [ ] Base de données PostgreSQL en production
- [ ] Migrations de base de données exécutées
- [ ] Tests automatisés validés
- [ ] Monitoring et logging configurés
- [ ] Backups automatiques de la base de données

## 📈 Évolutions Futures

### Fonctionnalités Avancées
- **Intégration email** (envoi automatique de candidatures)
- **Calendrier** d'entretiens intégré
- **Notifications push** pour les suivis
- **Export PDF** des candidatures
- **Intégration API** avec job boards
- **Machine Learning** pour recommandations
- **Mobile app** avec React Native

### Améliorations UX
- **Dark mode** complet
- **Thèmes personnalisables**
- **Raccourcis clavier** avancés
- **Glisser-déposer** pour organisation
- **Recherche intelligente** avec IA
- **Synchronisation multi-device**

---

*Application développée pour optimiser le processus de recherche d'emploi et maximiser les chances de succès des candidatures.*