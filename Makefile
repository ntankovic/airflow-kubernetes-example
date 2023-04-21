release_name := airflow
namespace := airflow
dag_image := cantab-dags
dag_image_version := 0.0.2
web_port := 9091

# dodati i još jedan job za dashboard
# https://kubernetes.io/docs/tasks/access-application-cluster/web-ui-dashboard/

build:
	docker build --pull --tag $(dag_image):$(dag_image_version) .

init: 
	helm repo add apache-airflow https://airflow.apache.org
	helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace

deploy:
	RELEASE_NAME=airflow

	helm upgrade $(release_name) apache-airflow/airflow --namespace $(namespace) \
    --set images.airflow.repository=$(dag_image) \
    --set images.airflow.tag=$(dag_image_version)

serve:
	@echo "Serving on http://localhost:$(web_port)"
	kubectl port-forward svc/airflow-webserver $(web_port):8080 --namespace $(namespace)

all: build deploy serve