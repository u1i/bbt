key=$(cat key.txt)

endpoint="southeastasia.api.cognitive.microsoft.com"

if [ "$#" = "0" ]
then
	echo need parameter: PIC URL
	exit
fi

pic=$1

curl -H "Content-Type: application/json" -H "Host: $endpoint" -H "Ocp-Apim-Subscription-Key: $key" -X POST -d "{ 'url':'$pic' }" "https://$endpoint/vision/v1.0/describe?visualFeatures=Description"
