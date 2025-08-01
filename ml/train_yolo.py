from ultralytics import YOLO
import os

# === 1. Carregar modelo ===
model = YOLO('yolov8l-pose.pt')  # Troque por 'm', 'l', etc. conforme necessidade

# === 2. Verificar dataset YAML ===
data_yaml = '/mnt/hd2/datasets/proj-neonatal/yolo_dataset/neonatal_18key.v1i.yolov8/data.yaml'
if not os.path.exists(data_yaml):
    raise FileNotFoundError(f"Arquivo não encontrado: {data_yaml}")

# === 3. Treinamento com pastas padrão ===
results = model.train(
    data=data_yaml,
    epochs=100,
    imgsz=768,
    batch=8,
    workers=8,
    device=0,

    # Otimização
    optimizer='AdamW',
    lr0=5e-4,
    lrf=0.01,
    weight_decay=5e-4,
    cos_lr=True,

    # Validação/salvamento
    val=True,
    save=True,
    save_period=10,
    exist_ok=True,      # Permite múltiplos runs sem erro

    # Early stopping
    patience=30,

    # Aumentos leves
    hsv_h=0.015,
    hsv_s=0.7,
    hsv_v=0.4,
    scale=0.4,
    shear=2,
    perspective=0.0005,

    # Outros
    amp=True,
    seed=42
)

# === 4. Pós-treino ===
print("✅ Treinamento concluído!")
print(f"📂 Resultados salvos em: {results.save_dir}")


# 5. Validação final (opcional, mas útil)
metrics = model.val()
print("📊 Métricas de validação:")
print(f" - mAP50-95 (caixa): {metrics.box.map:.4f}")
print(f" - mAP50 (caixa):    {metrics.box.map50:.4f}")
print(f" - mAP50-95 (pose):  {metrics.pose.map:.4f}")
print(f" - mAP50 (pose):     {metrics.pose.map50:.4f}")