import Link from 'next/link'

import { AppShell } from '@/components/app-shell'
import { Card } from '@/components/ui/card'
import { apiGet } from '@/lib/api'

export default async function IikoPage({
  searchParams,
}: {
  searchParams?: { organizationId?: string }
}) {
  const selectedFromQuery = searchParams?.organizationId
  let overview: any = {
    connection_status: 'error',
    token_received: false,
    organizations: [],
    organizations_found: 0,
    selected_organization: null,
    selected_organization_id: '',
    terminal_groups: [],
    terminal_groups_found: 0,
    products_loaded: 0,
    revision: 0,
  }
  let errorMessage = ''

  try {
    const query = selectedFromQuery ? `?organization_id=${encodeURIComponent(selectedFromQuery)}` : ''
    overview = await apiGet(`/api/integrations/iiko/overview${query}`)
  } catch (error) {
    errorMessage = error instanceof Error ? error.message : 'Network error: failed to connect to iiko API'
  }

  return (
    <AppShell>
      <Card className='mb-4'>
        <h2 className='text-xl font-semibold'>iikoCloud интеграция</h2>
        <p className='mt-1 text-sm text-slate-400'>Проверка подключения, организаций, terminal groups и nomenclature.</p>
      </Card>

      {errorMessage ? (
        <div className='mb-3 rounded-xl border border-red-600/30 bg-red-500/10 px-4 py-2 text-sm text-red-200'>
          {errorMessage}
        </div>
      ) : null}

      <div className='grid gap-4 md:grid-cols-2 xl:grid-cols-3'>
        <Card><p className='text-slate-400'>Connection status</p><p className='mt-2 text-lg font-semibold'>{overview.connection_status}</p></Card>
        <Card><p className='text-slate-400'>Token received</p><p className='mt-2 text-lg font-semibold'>{overview.token_received ? 'yes' : 'no'}</p></Card>
        <Card><p className='text-slate-400'>Organizations found</p><p className='mt-2 text-lg font-semibold'>{overview.organizations_found}</p></Card>
        <Card><p className='text-slate-400'>Selected organization</p><p className='mt-2 text-sm font-semibold'>{overview.selected_organization?.name || 'not selected'}</p><p className='text-xs text-slate-400'>{overview.selected_organization_id || '-'}</p></Card>
        <Card><p className='text-slate-400'>Terminal groups found</p><p className='mt-2 text-lg font-semibold'>{overview.terminal_groups_found}</p></Card>
        <Card><p className='text-slate-400'>Products loaded / Revision</p><p className='mt-2 text-lg font-semibold'>{overview.products_loaded} / {overview.revision}</p></Card>
      </div>

      <Card className='mt-4'>
        <div className='mb-3 flex items-center justify-between'>
          <h3 className='text-lg font-semibold'>Organizations</h3>
          <span className='text-xs text-slate-400'>Выберите организацию для загрузки terminal groups и nomenclature</span>
        </div>
        <div className='flex flex-wrap gap-2'>
          {(overview.organizations || []).map((org: any) => {
            const active = org.id === overview.selected_organization_id
            return (
              <Link
                key={org.id}
                href={`/iiko?organizationId=${org.id}`}
                className={`rounded-lg border px-3 py-2 text-sm ${active ? 'border-blue-400 bg-blue-500/20 text-blue-200' : 'border-slate-700 text-slate-300 hover:bg-slate-800'}`}
              >
                {org.name}
              </Link>
            )
          })}
        </div>
      </Card>
    </AppShell>
  )
}
