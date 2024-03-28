import { createLazyFileRoute } from '@tanstack/react-router'
import Navbar from '../components/Common/Navbar'

export const Route = createLazyFileRoute('/')({
  component: Index,
})

function Index() {
  return (
    <div className="p-2">
      <h3>Welcome Home!</h3>

      <Navbar/>
    </div>
  )
}