import pymeshlab


# Test model 1
fn1 = r"C:\Users\kyle\Downloads\RSI_APOLLO_TRIAGE.ctm"
ms1 = pymeshlab.MeshSet()
ms1.load_new_mesh(fn1)
ms1.save_current_mesh(fn1.split('.')[0] + '.stl')
ms1.save_current_mesh(fn1.split('.')[0] + '.obj')

# Test model 2
fn2 = r"C:\Users\kyle\Downloads\drake-cutlass_Cutlass-Black.ctm"
ms2 = pymeshlab.MeshSet()
ms2.load_new_mesh(fn2)
ms2.save_current_mesh(fn2.split('.')[0] + '.stl')
ms2.save_current_mesh(fn2.split('.')[0] + '.obj')
